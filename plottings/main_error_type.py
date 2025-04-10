import os

os.chdir("..")


import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from npeval import metrics
from npeval import plot_utils
from npeval.interval import get_interval_estimates
import pickle

import os.path as osp
from pathlib import Path

from npgym import NPEnv, PROBLEMS, PROBLEM_LEVELS
from npsolver.solver import extract_solution_from_response

import seaborn as sns

import os

getcwd = os.getcwd()
print(getcwd)


def get_data_with_try(problem, levels, model):
    seeds = [42, 53, 64]
    results = {}
    # min_len = len(levels)

    model_to_file = {
        "qwq-32b": "qwq",
        "deepseek-r1-32b": "deepseek-r1-32",
        "gpt-4o-mini": "gpt-4o-mini",
        "gpt-4o": "gpt-4o",
        "claude": "claude",
        "deepseek-v3": "deepseek-v3",
        "deepseek-r1": "deepseek-r1",
        "o1-mini": "o1-mini",
        "deepseek-v3-2503": "deepseek-v3-2503",
        "o3-mini": "o3-mini",
    }

    for seed in seeds:
        results[seed] = []

        for level in levels:
            dict_as_key = tuple(sorted(PROBLEM_LEVELS[problem][level].items()))

            new_result_file_template = "./full_results_flex/{}/{}/model_{}_problem_{}_level_{}_shots_1_seed_{}.pkl"

            f = open(
                new_result_file_template.format(
                    problem,
                    model_to_file[model],
                    model_to_file[model],
                    problem,
                    dict_as_key,
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
                # instances.append(data[level][i]["instance"])

                predicted_solution, _ = extract_solution_from_response(
                    data[i]["response"]
                )

                # if "response" in data[level][i].keys():
                #     predicted_solution, _ = extract_solution_from_response(
                #         data[level][i]["response"]
                #     )
                # else:
                #     print("miss of the response: {}, {}, {}, {}".format(model, problem, level, seed))
                #     predicted_solution = None
                # print(data[level][i]["response"])
                correctness.append([data[i]["instance"], predicted_solution])
            # print("level {}, accuracy = {}".format(level, true_num / 30))
            results[seed].append(correctness)
    return results


model_list = [
    "qwq-32b",
    "deepseek-r1-32b",
    "gpt-4o-mini",
    "gpt-4o",
    "claude",
    "deepseek-v3",
    "deepseek-v3-2503",
    "deepseek-r1",
    "o1-mini",
    "o3-mini",
]

MODEL2FIG = {
    "deepseek-r1-32b": "DeepSeek-R1-32B",
    "qwq-32b": "QwQ-32B",
    "gpt-4o-mini": "GPT-4o-mini",
    "gpt-4o": "GPT-4o",
    "claude": "Claude 3.7 Sonnet",
    "deepseek-v3": "DeepSeek-V3",
    "deepseek-r1": "DeepSeek-R1",
    "o1-mini": "o1-mini",
    "o3-mini": "o3-mini",
    "deepseek-v3-2503": "deepseek-v3-2503",
}

for problem_idx in [0, 1, 8, 9, 11, 12, 15, 16, 19, 22, 23, 24]:
    # if problem_idx not in [0]:
    #     continue
    problem = PROBLEMS[problem_idx]
    levels = list(PROBLEM_LEVELS[problem])

    colors = sns.color_palette("colorblind")

    fig, axes = plt.subplots(nrows=2, ncols=5, figsize=(5 * 5, 3.5 * 2))
    idx2errors = []
    model_level_errors = {}
    for m_idx, model in enumerate(model_list):
        # fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(3.5, 3.5 * 2))

        nppc_result = get_data_with_try(problem, levels, model)

        # print(nppc_result)
        # errors2idx = []

        levels2errors = [{} for _ in levels]
        for level in levels:
            # print(model, level, problem)
            env = NPEnv(problem_name=problem, level=level)

            instances = []
            solutions = []

            try:
                for seed in [42, 53, 64]:
                    instances += [result[0] for result in nppc_result[seed][level - 1]]
                    solutions += [result[1] for result in nppc_result[seed][level - 1]]

                verify_results = env.batch_verify_solution(instances, solutions)

                for result in verify_results:
                    # print(result[0])
                    if result[0]:
                        continue
                    else:
                        error = result[1].split(":")[0]
                        # print(error)
                        if error not in idx2errors:
                            idx2errors.append(error)

                        if error in levels2errors[level - 1]:
                            levels2errors[level - 1][error] += 1
                        else:
                            levels2errors[level - 1][error] = 1
            except:
                continue
        model_level_errors[model] = levels2errors

    error_list = []
    all_error_list = ["The solution is None", "VERIFICATION"]

    for error in idx2errors:
        if error not in all_error_list:
            error_list.append(error)
    error_list = sorted(error_list)
    all_error_list += error_list
    print(all_error_list)

    for m_idx, model in enumerate(model_list):
        levels2errors = model_level_errors[model]
        bottom = np.zeros([len(levels)])
        # fig, ax = plt.subplots()
        width = 1.0
        r_idx = m_idx // 5
        c_idx = m_idx % 5
        ax = axes[r_idx][c_idx]
        for i, error in enumerate(all_error_list):
            # ranks = all_ranks[task]
            current_errors = [
                (
                    levels2errors[level - 1][error]
                    if error in levels2errors[level - 1]
                    else 0
                )
                for level in levels
            ]
            ax.bar(
                [level for level in levels],
                current_errors,
                width,
                color=colors[i],
                bottom=bottom,
                alpha=0.9,
                edgecolor="white",
                linewidth=1.5,
                label="{}".format(error) if m_idx == 0 else None,
            )
            bottom += current_errors
        ax.set_title(f"{MODEL2FIG[model]}", fontsize=24)
        ax.tick_params(
            axis="both", which="major", labelsize=24
        )  # Set font size to 14 for top row
        # ax.legend(fontsize=18, ncol=1, loc="upper left")
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.set_xticks(levels)
        ax.set_ylim(0, 100)
        if c_idx != 0:
            ax.set_yticklabels([])
    fake_patches = [
        mpatches.Patch(color=colors[i], alpha=0.75) for i in range(len(all_error_list))
    ]
    legend = fig.legend(
        fake_patches,
        ["JSON ERROR", "VERIFICATION ERROR"] + all_error_list[2:],
        loc="upper center",
        fancybox=True,
        ncol=min(4, len(all_error_list)),
        fontsize=24,
        bbox_to_anchor=(0.5, 0),
    )
    plt.tight_layout()

    fig_folder = "./plottings/errors"
    file_name = fig_folder + "/errors_{}.pdf".format(problem)
    plt.savefig(file_name, format="pdf", bbox_inches="tight")
    plt.show()
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
