import os
import re
import json
import importlib
import sys
import argparse
from nppc_prompt import nppc_template, example_and_solution, problem_descriptions
from nppc_problem import problem_levels, problem2path
from utils import seed_everything
import asyncio
from litellm import completion, acompletion
from pathlib import Path
import pickle
import os.path as osp

models = {
    "gpt-4o": "gpt-4o-2024-08-06",
    "gpt-4o-mini": "gpt-4o-mini-2024-07-18",
    "o1-mini": "o1-mini-2024-09-12",
    "deepseek-chat": "deepseek/deepseek-chat",
    "claude": "anthropic/claude-3-sonnet-20240229",
}


def get_instance_generator(problem_name):
    np_gym_folder = "./npgym/npc"

    if os.path.dirname(np_gym_folder) not in sys.path:
        sys.path.append(np_gym_folder)
    problem_path = problem2path[problem_name]
    generate_instance = importlib.import_module(problem_path).generate_instance
    verify_solution = importlib.import_module(problem_path).verify_solution

    return generate_instance, verify_solution


def set_api_keys():
    with open("../api_keys/openai_api_key.txt", "r") as file:
        openai_api_key = file.read().strip()
    with open("../api_keys/deepseek_api_key.txt", "r") as file:
        deepseek_api_key = file.read().strip()
    with open("../api_keys/claude_api_key.txt", "r") as file:
        claude_api_key = file.read().strip()
    os.environ["OPENAI_API_KEY"] = openai_api_key
    os.environ["DEEPSEEK_API_KEY"] = deepseek_api_key
    os.environ["ANTHROPIC_API_KEY"] = claude_api_key


def extract_solution_from_response(response):
    # find the json code
    match = re.findall(r"```json\n(.*?)\n```", response, re.DOTALL)
    if match:
        json_str = match[-1]
        try:
            # remove the single line comment
            json_str = re.sub(r"//.*$", "", json_str, flags=re.MULTILINE)
            # remove the multiple line comment
            json_str = re.sub(r"/\*[\s\S]*?\*/", "", json_str)
            data = json.loads(json_str)
            answer = data["solution"]
            return answer
        except (json.JSONDecodeError, KeyError, SyntaxError) as e:
            print(f"Error parsing JSON or answer field: {e}")
            return None
    else:
        print("No JSON found in the text.")
        return None


def save_outputs(outputs, model_inputs, filepath):
    formatted_outputs = []
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            try:
                formatted_outputs = json.load(f)
            except json.JSONDecodeError:
                formatted_outputs = []
    output_item = {"output": outputs, "model_input": model_inputs}
    formatted_outputs.append(output_item)

    with open(filepath, "w") as f:
        json.dump(formatted_outputs, f, indent=2)
    return output_item["output"]


def evaluate_llm(content, model):
    messages = [{"content": content, "role": "user"}]
    response = completion(model=models[model], messages=messages)
    return response


async def async_evaluate_llm(contents, model):
    async def call_gpt(prompt):
        response = await acompletion(
            model=models[model], messages=[{"role": "user", "content": prompt}]
        )
        return response

    return await asyncio.gather(*[call_gpt(content) for content in contents])


def get_results_from_api(contents, model):
    results = []
    try:
        print("Starting the asy calling of LLM")
        responses = asyncio.run(async_evaluate_llm(contents, model=model))
        print("End of calling LLM")
        for idx, response in enumerate(responses):
            token_numbers = {
                "prompt": response.usage.prompt_tokens,
                "completion": response.usage.completion_tokens,
            }
            prediction = response.choices[0].message.content
            predicted_solution = extract_solution_from_response(prediction)

            result = {
                "instance": instance,
                "examples": examples,
                "response": prediction,
                "solution": predicted_solution,
                "tokens": token_numbers,
            }
            # print(result)
            results.append(result)
        return results
    except Exception as e:
        print(f"Error calling the LLM: {e}")
        return None


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--seed",
        type=int,
        required=False,
        default=42,
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
        default=0,
        help="the problem name idx",
    )
    parser.add_argument(
        "--n_shots",
        type=int,
        required=False,
        default=3,
        help="number of in-context examples",
    )

    parser.add_argument(
        "--n_trials",
        type=int,
        required=False,
        default=50,
        help="number of trials for each level",
    )

    parser.add_argument(
        "--asy_batch_size",
        type=int,
        required=False,
        default=10,
        help="the problem name",
    )

    parser.add_argument(
        "--result_folder",
        type=str,
        required=False,
        default="results",
        help="folder path to store the results",
    )

    return parser.parse_args()


if __name__ == "__main__":
    set_api_keys()

    args = get_parser()
    seed_everything(args.seed)

    model = args.model

    args.problem = 2
    problem_name = list(problem_descriptions)[args.problem]
    problem_description = problem_descriptions[problem_name]
    generate_instance, verify_solution = get_instance_generator(problem_name)

    n_shots = args.n_shots
    n_trials = args.n_trials

    def create_demo_text(configs):
        demo_content = ""
        examples = []
        for i in range(n_shots):
            instance, solution = generate_instance(**configs)
            demo = example_and_solution.replace(
                "<example_problem>", "{}".format(instance)
            ).replace("<example_solution>", json.dumps(solution))
            demo_content += demo
            examples.append(instance)
        instance, solution = generate_instance(**configs)
        return demo_content, instance, examples

    result_folder_path = Path(args.result_folder)
    if not result_folder_path.exists():
        result_folder_path.mkdir(parents=True, exist_ok=True)

    results = {}
    saving_path = "model_{}_problem_{}_shots_{}.pkl".format(
        model, problem_name, n_shots
    )
    levels = problem_levels[problem_name]
    for level in list(levels.keys())[-3:-2]:
        configs = levels[level]

        results[level] = []

        instances = []
        contents = []
        for trial in range(n_trials):
            content = nppc_template.replace(
                "<problem_description>", problem_description
            ).replace("<problem_name>", problem_name)
            demo_content, instance, examples = create_demo_text(configs)
            content = content.replace("<in_context_examples>", demo_content).replace(
                "<problem_to_solve>", "{}".format(instance)
            )

            instances.append(instance)
            contents.append(content)

            if len(contents) == args.asy_batch_size or (trial == n_trials - 1):
                # This is only for the online api model
                batch_results = get_results_from_api(contents=contents, model=model)
                # TODO: @ruiyu, please add the local model implementation

                if batch_results:
                    for idx, result in enumerate(batch_results):
                        predicted_solution = result["solution"]
                        if predicted_solution is not None:
                            correctness, reason = verify_solution(
                                instances[idx], predicted_solution
                            )
                        else:
                            correctness = False
                            reason = "Wrong Format: We cannot parse the solution from the response."
                        result["correctness"] = correctness
                        result["reason"] = reason

                    results[level] += batch_results
                instances = []
                contents = []
        break

    for level in results.keys():
        results_for_level = results[level]

        print(
            "This is for {} of {}".format(
                problem_levels[problem_name][level], problem_name
            )
        )
        accuracy = []
        reason = []
        for result in results_for_level:
            accuracy.append(result["correctness"])
            reason.append(result["reason"])
            print(
                "{}, {}, {}".format(
                    result["correctness"], result["reason"], result["tokens"]
                )
            )

        print(
            "Accuracy is {} (all={})".format(
                sum(accuracy) / len(accuracy), len(accuracy)
            )
        )

    with open(osp.join(result_folder_path, saving_path), "wb") as f:
        pickle.dump(results, f)
