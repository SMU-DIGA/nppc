import os

from pathlib import Path
import pickle
import os.path as osp
from npgym import NPEnv, PROBLEMS, PROBLEM_LEVELS
from npsolver import NPSolver
from copy import deepcopy


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


def set_api_keys():
    with open("api_keys/openai_api_key.txt", "r") as file:
        openai_api_key = file.read().strip()
    with open("api_keys/deepseek_api_key.txt", "r") as file:
        deepseek_api_key = file.read().strip()
    with open("./api_keys/claude_api_key.txt", "r") as file:
        claude_api_key = file.read().strip()
    os.environ["OPENAI_API_KEY"] = openai_api_key
    os.environ["DEEPSEEK_API_KEY"] = deepseek_api_key
    os.environ["ANTHROPIC_API_KEY"] = claude_api_key

    with open("./api_keys/huoshan_api_key.txt", "r") as file:
        huoshan_api_key = file.read().strip()
    os.environ["ARK_API_KEY"] = huoshan_api_key


import argparse


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
        default="deepseek-r1",
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
        default=10,
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

    result_folder_path = Path(args.result_folder)
    if not result_folder_path.exists():
        result_folder_path.mkdir(parents=True, exist_ok=True)

    results = {}
    saving_path = "model_{}_problem_{}_shots_{}.pkl".format(
        model_name, problem_name, n_shots
    )

    levels = PROBLEM_LEVELS[problem_name]
    for level_idx, level in enumerate(list(levels.keys())):
        if level_idx <= len(list(levels.keys())) - 3:
            continue

        env = NPEnv(problem_name=problem_name, level=level)
        solver = NPSolver(problem_name=problem_name, model_name=model_name)
        if args.verbose:
            print("=" * 15)
            print("level {}".format(level))
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
            inputs.append(
                {"instance": all_problems[problem_idx][0], "examples": examples}
            )
            instances.append(all_problems[problem_idx][0])
            problem_idx += 1
        results[level] = deepcopy(inputs)

        #  get the result batch by batch
        batch_size = args.batch_size
        num_batches = n_trials // batch_size + (0 if n_trials % batch_size == 0 else 1)

        predicted_solutions = []
        for batch_idx in range(num_batches):
            if args.verbose:
                print("batch {} over all {} batches".format(batch_idx + 1, num_batches))

            start_idx = batch_size * batch_idx
            end_idx = min(batch_size * (batch_idx + 1), n_trials)

            # we will talke the max tries for both open and close models
            # basically, we will
            for try_idx in range(args.max_tries):
                outputs = solver.get_prediction(inputs=inputs[start_idx:end_idx])

                if outputs is None:
                    continue
                else:
                    for idx, output in enumerate(outputs):
                        predicted_solutions.append(output["solution"])
                        results[level][start_idx + idx].update(output)
                    break
            else:
                predicted_solutions += [None] * batch_size

        # verify all the results
        verifications = env.batch_verify_solution(instances, predicted_solutions)
        for idx in range(len(results[level])):
            results[level][idx]["correctness"] = verifications[idx][0]
            results[level][idx]["reason"] = verifications[idx][1]

        break

    with open(osp.join(result_folder_path, saving_path), "wb") as f:
        pickle.dump(results, f)

    if args.verbose:
        for level in results.keys():
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
                        result["correctness"], result["reason"], result["tokens"]
                    )
                )

            print(
                "Accuracy is {} (all={})".format(
                    sum(accuracy) / len(accuracy), len(accuracy)
                )
            )


if __name__ == "__main__":
    set_api_keys()

    args = get_parser()
    seed_everything(args.seed)
    main(args)
