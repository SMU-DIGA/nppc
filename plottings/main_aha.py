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


def check_aha_number(reasoning_content):
    return reasoning_content.lower().count("wait")


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
                        [
                            check_aha_number(
                                data[level][i]["full_response"]
                                .choices[0]
                                .message.reasoning_content
                            ),
                            data[level][i]["correctness"],
                        ]
                    )
                # print("level {}, accuracy = {}".format(level, true_num / 30))
                results[seed].append(tokens)
            except:
                continue
    return results


model_list = [
    # "qwq-32b",
    # "deepseek-r1-32b",
    # "gpt-4o-mini",
    # "gpt-4o",
    # "claude",
    # "deepseek-v3",
    "deepseek-r1",
    # "o1-mini",
]

fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(5 * 4, 3 * 3))

for p_idx, problem_idx in enumerate([0, 1, 8, 9, 11, 12, 15, 16, 19, 22, 23, 24]):
    # if problem_idx not in [16]:
    #     continue
    problem = PROBLEMS[problem_idx]
    levels = list(PROBLEM_LEVELS[problem])

    for m_idx, model in enumerate(model_list):
        # fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(3.5, 3.5 * 2))

        nppc_result = get_data_with_try(problem, levels, model)

        print(nppc_result)

        nppc_results_correct = [[] for level in levels]

        nppc_results_wrong = [[] for level in levels]

        for level in levels:
            for seed in [42, 53, 64]:
                for instance in nppc_result[seed][level - 1]:
                    if instance[1]:
                        nppc_results_correct[level - 1].append(instance[0])
                    else:
                        nppc_results_wrong[level - 1].append(instance[0])

        for i in range(len(levels)):
            row_idx = p_idx // 4
            col_idx = p_idx % 4
            axes[row_idx][col_idx].scatter(
                [i + 1] * len(nppc_results_correct[i]),
                nppc_results_correct[i],
                marker="o",
                color="b",
                facecolor="None",
                label="correct" if i == 0 else None,
            )
            axes[row_idx][col_idx].scatter(
                [i + 1] * len(nppc_results_wrong[i]),
                nppc_results_wrong[i],
                marker="o",
                color="r",
                facecolor="None",
                label="correct" if i == 0 else None,
            )

            axes[row_idx][col_idx].grid(True, linestyle="--", alpha=0.6)
            axes[row_idx][col_idx].set_xticks(levels)

            axes[row_idx][col_idx].set_title(f"{problem}", fontsize=24)
            axes[row_idx][col_idx].tick_params(axis="both", which="major", labelsize=24)

            # if col_idx != 0:
            #     axes[row_idx][col_idx].set_yticklabels([])

plt.tight_layout()

# plt.ylabel("Performance", fontsize=32)
# plt.title("Model Performance Over Time", fontsize=24, weight="bold")
fig_folder = "./aha"
file_name = fig_folder + "/aha_r1.pdf"
plt.savefig(file_name, format="pdf", bbox_inches="tight")

plt.show()
