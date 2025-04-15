import os

os.chdir("..")

import matplotlib.pyplot as plt
import numpy as np

from npeval import metrics
from npeval import plot_utils
from npeval.interval import get_interval_estimates
import pickle

import os.path as osp
from pathlib import Path

from npgym import PROBLEMS, PROBLEM_LEVELS, NPEnv
from npsolver.solver import extract_solution_from_response
import seaborn as sns

import os

getcwd = os.getcwd()
print(getcwd)

PROBLEM2FIG = {
    "3-Satisfiability (3-SAT)": "3SAT",  # 0
    "Vertex Cover": "Vertex Cover",  # 1
    "Clique": "clique",  # 2
    "Independent Set": "independent_set",  # 3
    "Partition": "partition",  # 4
    "Subset Sum": "subset_sum",  # 5
    "Set Packing": "set_packing",  # 6
    "Set Splitting": "set_splitting",  # 7
    "Shortest Common Superstring": "Superstring",  # 8
    "Quadratic Diophantine Equations": "QDE",  # 9
    "Quadratic Congruences": "quadratic_congruence",  # 10
    "3-Dimensional Matching (3DM)": "3DM",  # 11
    "Travelling Salesman (TSP)": "TSP",  # 12
    "Dominating Set": "domninating_set",  # 13
    "Hitting String": "hitting_string",  # 14
    "Hamiltonian Cycle": "Hamiltonian Cycle",  # 15
    "Bin Packing": "Bin Packing",  # 16
    "Exact Cover by 3-Sets (X3C)": "x3c",  # 17
    "Minimum Cover": "minimum_cover",  # 18
    "Graph 3-Colourability (3-COL)": "3-COL",  # 19
    "Clustering": "clustering",  # 20
    "Betweenness": "betweenness",  # 21
    "Minimum Sum of Squares": "Min Sum Square",  # 22
    "Bandwidth": "Bandwidth",  # 23
    "Maximum Leaf Spanning Tree": "Max Leaf Span Tree",  # 24
}


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

    env = NPEnv(problem_name=problem, level=1)

    for seed in seeds:
        results[seed] = []

        for level in levels:
            try:
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
                tokens = []

                tokens = []
                for i in range(30):
                    # if model == 'gpt-4o':
                    #     print(data[level][i]["instance"])
                    tokens.append(
                        check_aha_number(
                            data[i]["full_response"]
                            .choices[0]
                            .message.reasoning_content
                        )
                    )
                instances = []
                solutions = []
                for i in range(30):
                    # print(data[level][i])
                    # if model == 'gpt-4o':
                    #     print(data[level][i]["instance"])
                    instances.append(data[i]["instance"])
                    predicted_solution, _ = extract_solution_from_response(
                        data[i]["response"]
                    )
                    # print(data[level][i]["response"])
                    solutions.append(predicted_solution)

                verify_results = env.batch_verify_solution(instances, solutions)

                full_tokens = []

                for i in range(30):
                    full_tokens.append([tokens[i], verify_results[i][0]])
                # for i in range(30):
                #     # if model == 'gpt-4o':
                #     #     print(data[level][i]["instance"])
                #     # print(data[level][i]["full_response"].choices[0].message.reasoning_content)
                #     tokens.append(
                #         [
                #             check_aha_number(
                #                 data[i]["full_response"]
                #                 .choices[0]
                #                 .message.reasoning_content
                #             ),
                #             data[i]["correctness"],
                #         ]
                #     )
                # print("level {}, accuracy = {}".format(level, true_num / 30))
                results[seed].append(full_tokens)
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

colors = sns.color_palette("colorblind")

blind_blue = "b"
blind_red = "r"

correct_marker = "o"
wrong_marker = "x"

blind_green = colors[2]

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

        all_ahas = []
        for i in range(len(levels)):
            row_idx = p_idx // 4
            col_idx = p_idx % 4
            axes[row_idx][col_idx].scatter(
                [i + 1] * len(nppc_results_correct[i]),
                nppc_results_correct[i],
                marker=correct_marker,
                color="b",
                # facecolor="None",
                s=64,
                alpha=0.1,
                label="correct" if i == 0 else None,
            )
            axes[row_idx][col_idx].scatter(
                [i + 1] * len(nppc_results_wrong[i]),
                nppc_results_wrong[i],
                marker=wrong_marker,
                color="r",
                s=64,
                alpha=0.1,
                # facecolor="None",
                label="correct" if i == 0 else None,
            )

            all_ahas.append(
                (sum(nppc_results_wrong[i]) + sum(nppc_results_correct[i]))
                / (len(nppc_results_correct[i]) + len(nppc_results_wrong[i]))
            )

            axes[row_idx][col_idx].grid(True, linestyle="--", alpha=0.6)
            axes[row_idx][col_idx].set_xticks(levels)

            axes[row_idx][col_idx].set_ylim(0, 80)
            axes[row_idx][col_idx].set_yticks([i * 20 for i in range(5)])

            axes[row_idx][col_idx].set_title(f"{PROBLEM2FIG[problem]}", fontsize=24)
            axes[row_idx][col_idx].tick_params(axis="both", which="major", labelsize=24)

            axes[row_idx][col_idx].plot(
                [i + 1 for i in range(len(all_ahas))],
                all_ahas,
                color=blind_green,
                linewidth=4.5,
                alpha=0.75,
            )

            if col_idx != 0:
                axes[row_idx][col_idx].set_yticklabels([])
            else:
                pass
                # axes[row_idx][col_idx].set_ylabel('Number', position=(0, 0.5), rotation=90, fontsize=24)


plt.tight_layout()

# plt.ylabel("Performance", fontsize=32)
# plt.title("Model Performance Over Time", fontsize=24, weight="bold")
fig_folder = "./plottings/aha"
file_name = fig_folder + "/aha_r1.pdf"
plt.savefig(file_name, format="pdf", bbox_inches="tight")

plt.show()
