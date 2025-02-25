import os
import re
import json
import argparse
import multiprocessing as mp
import multiprocessing.pool
import multiprocessing.resource_tracker as rt
import logging
import ast
import gc
import importlib
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple, Callable, Optional

import torch
from huggingface_hub import snapshot_download
from vllm import LLM, SamplingParams
from litellm import batch_completion

from nppc_prompt import nppc_template, example_and_solution, problem_descriptions
from nppc_problem import problem_levels, problem2path
from utils import seed_everything

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Type aliases
ProblemInstance = str
Solution = List[Any]
ModelConfig = Dict[str, Any]
LLMResponse = Dict[str, Any]

MODELS = {
    # Online models
    "gpt-4o": "gpt-4o-2024-08-06",
    "gpt-4o-mini": "gpt-4o-mini-2024-07-18",
    "o1-mini": "o1-mini-2024-09-12",
    "deepseek-chat": "deepseek/deepseek-chat",
    # Offline models
    "deepseek": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
}

def get_instance_generator(problem_name: str, np_gym_folder: str = "./npgym/npc") -> Tuple[Callable, Callable]:
    """Load problem-specific instance generator and validator"""
    np_gym_dir = Path(np_gym_folder)
    if str(np_gym_dir) not in sys.path:
        sys.path.append(str(np_gym_dir))
        
    problem_path = problem2path[problem_name]
    module = importlib.import_module(problem_path)
    return module.generate_instance, module.verify_solution


def set_api_keys() -> None:
    """Load API keys from secure storage"""
    key_path = Path("api_keys")
    
    with (key_path / "openai_api_key.txt").open() as f:
        os.environ["OPENAI_API_KEY"] = f.read().strip()
    
    with (key_path / "deepseek_api_key.txt").open() as f:
        os.environ["DEEPSEEK_API_KEY"] = f.read().strip()


def extract_solution_from_response(response: str) -> Optional[List[Any]]:
    """Parse JSON solution from LLM response with error handling"""
    json_blocks = re.findall(r"```json\n(.*?)\n```", response, re.DOTALL)
    if not json_blocks:
        logger.warning("No JSON block found in response")
        return None

    try:
        json_str = re.sub(r"//.*$", "", json_blocks[-1], flags=re.MULTILINE)
        json_str = re.sub(r"/\*[\s\S]*?\*/", "", json_str)
        data = json.loads(json_str)
        
        solution = data.get("solution")
        if isinstance(solution, str):
            solution = ast.literal_eval(solution)
            
        if not isinstance(solution, list):
            logger.error("Solution is not a list")
            return None
            
        return solution
    except (json.JSONDecodeError, SyntaxError, ValueError) as e:
        logger.error(f"Failed to parse solution: {str(e)}")
        return None


def save_outputs(results: List[Dict], file_path: Path) -> None:
    """Save results to JSON file with atomic write, handling empty or corrupted files."""
    try:
        existing_data = []
        if file_path.exists():
            with file_path.open() as f:
                try:
                    existing_data = json.load(f)  # Load existing JSON
                except json.JSONDecodeError:
                    logger.warning(f"Warning: {file_path} is empty or corrupted. Overwriting with fresh results.")
                    existing_data = []  # Reset if file is corrupted
        
        def convert_sets(obj):
            """Ensure JSON compatibility by converting sets, tuples, and None values."""
            if isinstance(obj, set):
                return list(obj)  # Convert sets to lists
            elif isinstance(obj, tuple):
                return list(obj)  # Convert tuples to lists
            elif isinstance(obj, dict):
                return {str(k): convert_sets(v) for k, v in obj.items()}  # Ensure valid dict
            elif isinstance(obj, list):
                return [convert_sets(x) for x in obj]  # Recursively process lists
            elif obj is None:
                return "null"  # JSON cannot handle None, replace with "null"
            return obj
        existing_data += [convert_sets(r) for r in results]
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(
                existing_data,
                f,
                indent=2,
                ensure_ascii=False
            )
    except (IOError, json.JSONDecodeError) as e:
        logger.error(f"Failed to save results: {str(e)}")


def initialize_offline_model(model_name: str, model_dir: Path = Path("offline_models")) -> Tuple[LLM, SamplingParams]:
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / model_name
    
    if not model_path.exists():
        logger.info(f"Downloading {MODELS[model_name]}...")
        snapshot_download(
            repo_id=MODELS[model_name],
            local_dir=str(model_path),
            resume_download=True
        )
    else:
        print(f"\n{'='*20} Loading model from {str(model_path)} {'='*20}")

    device_count = torch.cuda.device_count()
    if device_count == 0:
        raise RuntimeError("No available GPUs found")
        
    return LLM(
        model=MODELS[model_name],
        download_dir=str(model_path),
        tensor_parallel_size=max(device_count, 1),
        dtype="auto",
        gpu_memory_utilization=0.8,
        trust_remote_code=True,
        enforce_eager=True
    ), SamplingParams(
        temperature=0.6,
        top_p=0.95,
        max_tokens=7500
    )


def process_batch(batch_instances: List[str], 
                 batch_contents: List[str],
                 verify_solution: Callable,
                 model_name: str,
                 llm: Optional[LLM],
                 sampling_params: Optional[SamplingParams]) -> List[Dict]:
    """Process a batch of instances through LLM"""
    offline_mode = False
    try:
        if llm is not None and sampling_params is not None:
            offline_mode = True
            responses = llm.generate(batch_contents, sampling_params)
        else:
            messages = [[{"role": "user", "content": content}] for content in batch_contents]
            responses = batch_completion(messages=messages, model=MODELS[model_name])
        return [
            format_response(response, instance, verify_solution, offline_mode)
            for response, instance in zip(responses, batch_instances)
        ]
    except Exception as e:
        logger.error(f"Batch processing failed: {str(e)}")
        return []


def format_response(response: Any, 
                   instance: str,
                   verify_solution: Callable,
                   offline_mode: bool) -> Dict:
    """Format LLM response with validation"""
    prediction = response.outputs[0].text if offline_mode else response.choices[0].message.content
    solution = extract_solution_from_response(prediction)
    
    if solution is not None:
        valid, reason = verify_solution(instance, solution)
    else:
        valid, reason = False, "Invalid solution format"
        
    return {
        "instance": instance,
        # "response": prediction,
        "solution": solution,
        "correctness": valid,
        "reason": reason,
        "tokens": {
            "prompt": len(response.prompt_token_ids) if offline_mode else response.usage.prompt_tokens,
            "completion": len(response.outputs[0].token_ids) if offline_mode else response.usage.completion_tokens,
        }
    }


def process_level(level: str,
                 problem_name: str,
                 result_folder: Path,
                 args: argparse.Namespace,
                #  llm: Optional[LLM],
                #  sampling_params: Optional[SamplingParams],
                 debug: bool = False) -> None:
    """Process a single problem level in isolated context"""
    with ResourceManager():
        logger.info(f"\n{'='*20} Processing level {level} {'='*20}")
        
        # Initialize components
        generate_instance, verify_solution = get_instance_generator(problem_name)
        configs = problem_levels[problem_name][level]
        if args.offline_eval:
            llm, sampling_params = initialize_offline_model(args.model)
        else: 
            llm, sampling_params = None, None
        # set seed after initializing offline model
        seed_everything(args.seed)
        
        # Generate evaluation instances
        instances = [generate_instance(**configs)[0] for _ in range(args.n_trials)]
        
        # Create prompt template
        demos = "\n".join(
            example_and_solution.replace("<example_problem>", "{}".format(inst)).replace("<example_solution>", json.dumps(sol))
            for inst, sol in (generate_instance(**configs) for _ in range(args.n_shots))
        )

        main_prompt = nppc_template.replace(
                "<problem_description>", problem_descriptions[problem_name]
            ).replace("<problem_name>", problem_name
            ).replace("<in_context_examples>", demos)
            
        # Process in batches
        results = []
        for batch_start in range(0, args.n_trials, args.asy_batch_size):
            batch_instances = instances[batch_start:batch_start+args.asy_batch_size]
            batch_prompts = [main_prompt.replace("<problem_to_solve>", "{}".format(inst)) for inst in batch_instances]
            
            if debug:
                print(f"\n{'='*20} Example Prompt {'='*20}\n{batch_prompts[0]}\n{'='*20} Example Prompt {'='*20}")
            
            batch_results = process_batch(
                batch_instances, batch_prompts, verify_solution, args.model, llm, sampling_params
            )
            
            if debug:
                print(f"\n{'='*20} Example Results {'='*20}\n{batch_results[0]}\n{'='*20} Example Results {'='*20}")
            
            save_outputs(batch_results, result_folder / f"shots_{args.n_shots}_level_{level}.json")
            results.extend(batch_results)
            
        # Calculate metrics
        accuracy = sum(r["correctness"] for r in results) / len(results) if results else 0
        logger.info(f"Level {level} accuracy: {accuracy:.2%} ({sum(r['correctness'] for r in results)}/{len(results)})")


def configure_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NPCC Evaluation Pipeline")
    parser.add_argument("--seed", type=int, default=42,
                       help="Random seed for reproducibility")
    parser.add_argument("--model", choices=list(MODELS), default="deepseek",
                       help="Model to evaluate")
    parser.add_argument("--problem", type=int, default=0,
                       help="Problem index to evaluate")
    parser.add_argument("-l", "--level", type=int, default=1,
                       help="Level of problem to evaluate")
    parser.add_argument("--n_shots", type=int, default=3,
                       help="Number of in-context examples")
    parser.add_argument("--n_trials", type=int, default=8,
                       help="Trials per difficulty level")
    parser.add_argument("--asy_batch_size", type=int, default=4,
                       help="Parallel evaluation batch size")
    parser.add_argument("--result_folder", type=Path, default="results",
                       help="Output directory for results")
    parser.add_argument("-o", "--offline_eval", action="store_true",
                       help="Use offline model evaluation")
    parser.add_argument("--debug", action="store_true",
                       help="Debug mode")
    return parser


def main():
    """Main execution flow"""
    args = configure_parser().parse_args()
    problem_name = list(problem_descriptions)[args.problem]
    if args.debug:
        print('='*20, f"Evaluating problem: {problem_name}", '='*20)
    result_folder = Path(args.result_folder) / f"{problem2path[problem_name]}" / f"{args.model}"
    result_folder.mkdir(parents=True, exist_ok=True)
    assert args.level in list(problem_levels[list(problem_descriptions)[args.problem]].keys())
    logger.info(f"\n{'='*20} Processing level {args.level} {'='*20}")
        
    # Initialize components
    generate_instance, verify_solution = get_instance_generator(problem_name)
    configs = problem_levels[problem_name][args.level]
    if args.offline_eval:
        llm, sampling_params = initialize_offline_model(args.model)
    else: 
        llm, sampling_params = None, None
    # set seed after initializing offline model
    seed_everything(args.seed)
    
    # Generate evaluation instances
    instances = [generate_instance(**configs)[0] for _ in range(args.n_trials)]
    
    # Create prompt template
    demos = "\n".join(
        example_and_solution.replace("<example_problem>", "{}".format(inst)).replace("<example_solution>", json.dumps(sol))
        for inst, sol in (generate_instance(**configs) for _ in range(args.n_shots))
    )

    main_prompt = nppc_template.replace(
            "<problem_description>", problem_descriptions[problem_name]
        ).replace("<problem_name>", problem_name
        ).replace("<in_context_examples>", demos)
        
    # Process in batches
    results = []
    for batch_start in range(0, args.n_trials, args.asy_batch_size):
        batch_end = batch_start+args.asy_batch_size if batch_start+args.asy_batch_size < args.n_trials else args.n_trials
        batch_instances = instances[batch_start:batch_end]
        batch_prompts = [main_prompt.replace("<problem_to_solve>", "{}".format(inst)) for inst in batch_instances]
        
        if args.debug:
            print(f"\n{'='*20} Example Prompt {'='*20}\n{batch_prompts[0]}\n{'='*20} Example Prompt {'='*20}")
        
        batch_results = process_batch(
            batch_instances, batch_prompts, verify_solution, args.model, llm, sampling_params
        )
        
        if args.debug:
            print(f"\n{'='*20} Example Results {'='*20}\n{batch_results[0]}\n{'='*20} Example Results {'='*20}")

        save_outputs(batch_results, result_folder / f"shots_{args.n_shots}_level_{args.level}.json")
        results.extend(batch_results)
        
    # Calculate metrics
    accuracy = sum(r["correctness"] for r in results) / len(results) if results else 0
    logger.info(f"Level {args.level} accuracy: {accuracy:.2%} ({sum(r['correctness'] for r in results)}/{len(results)})")
    res_summary = [{
        "level": f"{args.level}",
        "accuracy": f"{accuracy}",
        "num rollouts": f"{len(results)}",
    }]
    save_outputs(res_summary, result_folder / f"shots_{args.n_shots}_summary.json")

if __name__ == "__main__":
    main()