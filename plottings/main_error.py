import matplotlib.pyplot as plt
import numpy as np

from npeval import metrics
from npeval import plot_utils
from npeval.interval import get_interval_estimates
import pickle

import os.path as osp
from pathlib import Path

from npgym import NPEnv, PROBLEMS, PROBLEM_LEVELS

import seaborn as sns

import os

getcwd = os.getcwd()
print(getcwd)


def get_data_with_try(problem, levels, model):
    seeds = [42, 53, 64]
    results = {}
    min_len = len(levels)

    model_to_file = {
        "qwq-32b": "qwq",
        "deepseek-r1-32b": "deepseek-r1-32",
        "gpt-4o-mini": "gpt-4o-mini",
        "gpt-4o": "gpt-4o",
        "claude": "claude",
        "deepseek-v3": "deepseek-v3",
        "deepseek-r1": "deepseek-r1",
        "o1-mini": "o1-mini",
    }

    for seed in seeds:
        results[seed] = []

        for level in levels:
            try:
                if model in ["deepseek-r1"]:
                    result_file_template = "../results_r1/{}/{}/model_{}_problem_{}_level_{}_shots_1_seed_{}.pkl"
                else:
                    result_file_template = "../results/{}/{}/model_{}_problem_{}_level_{}_shots_1_seed_{}.pkl"
                f = open(
                    result_file_template.format(
                        problem,
                        model_to_file[model],
                        model_to_file[model],
                        problem,
                        level,
                        seed,
                    ),
                    "rb",
                )
                data = pickle.load(f)
                correctness = []
                for i in range(30):
                    # print(data[level][i])
                    # if model == 'gpt-4o':
                    #     print(data[level][i]["instance"])
                    correctness.append(
                        [data[level][i]["instance"], data[level][i]["solution"]]
                    )
                # print("level {}, accuracy = {}".format(level, true_num / 30))
                results[seed].append(correctness)
            except:
                continue
    return results


model_list = [
    # "qwq-32b",
    # "deepseek-r1-32b",
    "gpt-4o-mini",
    "gpt-4o",
    "claude",
    "deepseek-v3",
    "deepseek-r1",
    "o1-mini",
]

for problem_idx in [0, 1, 8, 9, 11, 12, 15, 16, 19, 22, 23, 24]:
    # if problem_idx not in [16]:
    #     continue
    problem = PROBLEMS[problem_idx]
    levels = list(PROBLEM_LEVELS[problem])

    fig, axes = plt.subplots(nrows=2, ncols=6, figsize=(5 * 6, 3 * 2))
    for m_idx, model in enumerate(model_list):
        # fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(3.5, 3.5 * 2))

        nppc_result = get_data_with_try(problem, levels, model)

        # print(nppc_result)
        for level in levels:
            print(model, level, problem)
            env = NPEnv(problem_name=problem, level=level)

            instances = []
            solutions = []

            for seed in [42, 53, 64]:
                instances += [result[0] for result in nppc_result[seed][level - 1]]
                solutions += [result[0] for result in nppc_result[seed][level - 1]]

            verify_results = env.batch_verify_solution(instances, solutions)

            print(verify_results)

        # print(nppc_result)

        # error_keys = []
        # error_key_indices = {}
        # level_to_errors = [[] for i in levels]
        #
        # for seed in [42, 53, 64]:
        #     for level in levels:
        #         level_to_errors[level - 1] = {}
        #         for instance in nppc_result[seed][level - 1]:
        #             if instance[0]:
        #                 continue
        #             else:
        #                 if instance[1] in level_to_errors[level - 1]:
        #                     level_to_errors[level - 1][instance[1]] += 1
        #                 else:
        #                     level_to_errors[level - 1][instance[1]] = 1
        #
        # print(level_to_errors)

    # plt.tight_layout()
    #
    # # plt.ylabel("Performance", fontsize=32)
    # # plt.title("Model Performance Over Time", fontsize=24, weight="bold")
    # fig_folder = './tokens'
    # file_name = fig_folder + "/tokens_{}.pdf".format(problem)
    # plt.savefig(file_name, format="pdf", bbox_inches="tight")
    #
    # plt.show()
    # break

    # if problem_idx == 9:
    #     levels = levels[:9]
    # fig, ax = plt.subplots(figsize=(7, 5))
    #
    # for model in model_list:
    #     plot_one_line(ax=ax, model=model, colors=colors, levels=levels, problem=problem)
    # # ax.set_xscale('log')
    # plt.tight_layout()
    #
    # plots_folder = "./performance_over_levels"
    # path_plots_folder = Path(plots_folder)
    # if not path_plots_folder.exists():
    #     path_plots_folder.mkdir(parents=True, exist_ok=True)
    # plt.savefig(
    #     osp.join(plots_folder, "{}.pdf".format(problem)),
    #     bbox_inches="tight",
    #     pad_inches=0.0,
    # )
    # plt.show()
