import os
import os.path as osp
import pickle
import time
from copy import deepcopy
from pathlib import Path
import torch
import gc

from npgym import NPEnv, PROBLEMS, PROBLEM_LEVELS
from npsolver import MODELS
from npsolver.solver import NPSolver


def seed_everything(seed=42):
    import torch
    import numpy as np
    import random

    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(seed)
    random.seed(seed)


import os


def set_api_keys():
    def load_key(file_path: str):
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return f.read().strip()
        return None

    # Required keys
    openai_key = load_key("api_keys/openai_api_key.txt")
    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key

    huoshan_key = load_key("api_keys/huoshan_api_key.txt")
    if huoshan_key:
        os.environ["ARK_API_KEY"] = huoshan_key

    # Optional keys
    deepseek_key = load_key("api_keys/deepseek_api_key.txt")
    if deepseek_key:
        os.environ["DEEPSEEK_API_KEY"] = deepseek_key

    claude_key = load_key("api_keys/claude_api_key.txt")
    if claude_key:
        os.environ["ANTHROPIC_API_KEY"] = claude_key

    maas_key = load_key("api_keys/maas_api_key.txt")
    if maas_key:
        os.environ["MAAS_API_KEY"] = maas_key


import argparse


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--seed",
        type=int,
        required=False,
        default=64,
        help="seed",
    )
    parser.add_argument(
        "--model",
        type=str,
        required=False,
        default="claude",
        help="name for LLM",
    )
    parser.add_argument(
        "--problem",
        type=int,
        required=False,
        default=11,
        help="the problem name idx",
    )

    parser.add_argument(
        "--level",
        type=int,
        required=False,
        default=1,
        help="level",
    )

    parser.add_argument(
        "--n_shots",
        type=int,
        required=False,
        default=1,
        help="number of in-context examples",
    )

    parser.add_argument(
        "--n_trials",
        type=int,
        required=False,
        default=30,
        help="number of trials for each level",
    )

    parser.add_argument(
        "--batch_size",
        type=int,
        required=False,
        default=1,
        help="the problem name",
    )

    parser.add_argument(
        "--max_tries",
        type=int,
        required=False,
        default=3,
        help="max tries for one batch",
    )

    parser.add_argument(
        "--result_folder",
        type=str,
        required=False,
        default="results",
        help="folder path to store the results",
    )

    parser.add_argument("--verbose", type=bool, required=False, default=True)

    return parser.parse_args()


def main(args):
    model_name = args.model

    problem_name = PROBLEMS[args.problem]

    n_shots = args.n_shots
    n_trials = args.n_trials
    level = args.level

    levels = PROBLEM_LEVELS[problem_name]
    assert level in levels

    result_folder_path = Path(args.result_folder)
    if not result_folder_path.exists():
        result_folder_path.mkdir(parents=True, exist_ok=True)

    result_folder_path_per_problem = Path(osp.join(args.result_folder, problem_name))
    if not result_folder_path_per_problem.exists():
        result_folder_path_per_problem.mkdir(parents=True, exist_ok=True)

    result_folder_path_per_model = Path(
        osp.join(args.result_folder, problem_name, model_name)
    )
    if not result_folder_path_per_model.exists():
        result_folder_path_per_model.mkdir(parents=True, exist_ok=True)

    dict_as_key = tuple(sorted(PROBLEM_LEVELS[problem_name][level].items()))

    results = {}
    saving_path = "model_{}_problem_{}_level_{}_shots_{}_seed_{}.pkl".format(
        model_name, problem_name, dict_as_key, n_shots, args.seed
    )

    env = NPEnv(problem_name=problem_name, level=level)
    solver = NPSolver(problem_name=problem_name, model_name=model_name, seed=args.seed)

    if args.verbose:
        print("=" * 15)
        print("level {}: {}".format(level, levels[level]))
        print("=" * 15)

    # generate all the instance, examples and contents
    inputs = []
    instances = []

    all_problems = env.batch_generate_instance((n_shots + 1) * n_trials)

    problem_idx = 0
    for _ in range(n_trials):
        examples = []
        for _ in range(n_shots):
            examples.append(all_problems[problem_idx])
            problem_idx += 1
        inputs.append({"instance": all_problems[problem_idx][0], "examples": examples})
        instances.append(all_problems[problem_idx][0])
        problem_idx += 1
    results[level] = deepcopy(inputs)

    #  get the result batch by batch
    batch_size = args.batch_size
    num_batches = n_trials // batch_size + (0 if n_trials % batch_size == 0 else 1)

    predicted_solutions = []

    is_llm_error = False
    for batch_idx in range(num_batches):
        if args.verbose:
            print("batch {} over all {} batches".format(batch_idx + 1, num_batches))

        start_idx = batch_size * batch_idx
        end_idx = min(batch_size * (batch_idx + 1), n_trials)

        # we will talke the max tries for both open and close models

        for try_idx in range(args.max_tries):
            outputs = solver.get_prediction(inputs=inputs[start_idx:end_idx])

            if not outputs[0]["error_msg"]["llm"] or try_idx == args.max_tries - 1:
                for idx, output in enumerate(outputs):
                    predicted_solutions.append(output["solution"])
                    results[level][start_idx + idx].update(output)
                break
            time.sleep(20)

    # verify all the results
    verifications = env.batch_verify_solution(instances, predicted_solutions)
    for idx in range(len(results[level])):
        results[level][idx]["correctness"] = verifications[idx][0]
        results[level][idx]["reason"] = verifications[idx][1]

    if args.verbose:
        results_for_level = results[level]

        print(
            "This is for {} of {}".format(
                PROBLEM_LEVELS[problem_name][level], problem_name
            )
        )
        accuracy = []
        reason = []

        for result in results_for_level:
            accuracy.append(result["correctness"])
            reason.append(result["reason"])
            print(
                "{}, {}, {}".format(
                    result["correctness"],
                    result["reason"],
                    result["tokens"] if "tokens" in result.keys() else 0,
                )
            )

            if "tokens" not in result.keys():
                is_llm_error = True

        print(
            "Accuracy is {} (all={})".format(
                sum(accuracy) / len(accuracy), len(accuracy)
            )
        )
    if not is_llm_error:
        with open(osp.join(result_folder_path_per_model, saving_path), "wb") as f:
            pickle.dump(results[level], f)

    if not solver.is_online:
        from vllm.distributed.parallel_state import destroy_model_parallel

        destroy_model_parallel()
        del solver.local_llm.llm_engine.model_executor.driver_worker
        del solver.local_llm
        gc.collect()
        torch.cuda.empty_cache()


if __name__ == "__main__":
    set_api_keys()

    args = get_parser()

    problem_name = PROBLEMS[args.problem]
    levels = PROBLEM_LEVELS[problem_name]

    for seed in [64]:
        args.seed = seed
        for level in levels:
            if level not in [1, 2]:
                continue
            seed_everything(args.seed)
            args.level = level
            print(args)
            main(args)
