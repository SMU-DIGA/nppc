import matplotlib.pyplot as plt
import numpy as np

from npeval import metrics
from npeval import plot_utils
from npeval.interval import get_interval_estimates
import pickle

import os.path as osp
from pathlib import Path

from npgym import PROBLEMS, PROBLEM_LEVELS

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
                tokens = []
                for i in range(30):
                    # if model == 'gpt-4o':
                    #     print(data[level][i]["instance"])
                    tokens.append(
                        [data[level][i]["tokens"], data[level][i]["correctness"]]
                    )
                # print("level {}, accuracy = {}".format(level, true_num / 30))
                results[seed].append(tokens)
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

        correct_prompt = []
        wrong_prompt = []
        correct_completion = []
        wrong_completion = []

        for i in range(len(levels)):
            correct_prompt.append([])
            wrong_prompt.append([])
            correct_completion.append([])
            wrong_completion.append([])

            for seed in [42, 53, 64]:
                if i >= len(nppc_result[seed]):
                    continue
                for j in range(len(nppc_result[seed][i])):
                    if nppc_result[seed][i][j][1]:
                        correct_prompt[-1].append(nppc_result[seed][i][j][0]["prompt"])
                        correct_completion[-1].append(
                            nppc_result[seed][i][j][0]["completion"]
                        )
                    else:
                        wrong_prompt[-1].append(nppc_result[seed][i][j][0]["prompt"])
                        wrong_completion[-1].append(
                            nppc_result[seed][i][j][0]["completion"]
                        )

        # axes[1].xlim(0, len(levels)+1)
        # axes[1].ylim(0, 10)

        for i in range(len(levels)):
            axes[0][m_idx].scatter(
                [i + 1] * len(correct_prompt[i]),
                correct_prompt[i],
                marker="o",
                color="b",
                facecolor="None",
                label="correct" if i == 0 else None,
            )

            axes[0][m_idx].scatter(
                [i + 1] * len(wrong_prompt[i]),
                wrong_prompt[i],
                marker="o",
                color="r",
                facecolor="None",
                label="wrong" if i == 0 else None,
            )

            axes[0][m_idx].legend(fontsize=18, ncol=1, loc="upper left")
            axes[0][m_idx].grid(True, linestyle="--", alpha=0.6)
            axes[0][m_idx].set_xticks(levels)
            # if m_idx != 0:
            #     axes[0][m_idx].set_yticklabels([])

            # axes[0][m_idx].set_xticks(fontsize=32)
            # axes[0][m_idx].set_yticks(fontsize=32)
            axes[0][m_idx].set_title(f"{model}", fontsize=24)
            axes[0][m_idx].tick_params(
                axis="both", which="major", labelsize=24
            )  # Set font size to 14 for top row

        for i in range(len(levels)):
            axes[1][m_idx].scatter(
                [i + 1] * len(correct_completion[i]),
                correct_completion[i],
                marker="o",
                color="b",
                facecolor="None",
                # label='correct' if i == 0 else None
            )

            axes[1][m_idx].scatter(
                [i + 1] * len(wrong_completion[i]),
                wrong_completion[i],
                marker="o",
                color="r",
                facecolor="None",
                # label='correct' if i == 0 else None
            )

            # axes[1][m_idx].legend(fontsize=18, ncol=1, loc="upper left")
            axes[1][m_idx].grid(True, linestyle="--", alpha=0.6)
            axes[1][m_idx].set_xticks(levels)

            # if m_idx != 0:
            #     axes[1][m_idx].set_yticklabels([])

            # axes[1][m_idx].set_yticks(fontsize=32)
            axes[1][m_idx].tick_params(axis="both", which="major", labelsize=24)

    plt.tight_layout()

    # plt.ylabel("Performance", fontsize=32)
    # plt.title("Model Performance Over Time", fontsize=24, weight="bold")
    fig_folder = "./tokens"
    file_name = fig_folder + "/tokens_{}.pdf".format(problem)
    plt.savefig(file_name, format="pdf", bbox_inches="tight")

    plt.show()
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
