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

from npgym import PROBLEMS, PROBLEM_LEVELS

import seaborn as sns
from npgym import NPEnv, PROBLEMS, PROBLEM_LEVELS
from npsolver.solver import extract_solution_from_response
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
        "deepseek-v3-2503": "deepseek-v3-2503",
        "deepseek-r1": "deepseek-r1",
        "o1-mini": "o1-mini",
        "o3-mini": "o3-mini",
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
                for i in range(30):
                    # if model == 'gpt-4o':
                    #     print(data[level][i]["instance"])
                    tokens.append(data[i]["tokens"])
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

                # print("level {}, accuracy = {}".format(level, true_num / 30))
                results[seed].append(full_tokens)
            except:
                continue
    return results


MODEL2FIG = {
    "deepseek-r1-32b": "DeepSeek-R1-32B",
    "qwq-32b": "QwQ-32B",
    "gpt-4o-mini": "GPT-4o-mini",
    "gpt-4o": "GPT-4o",
    "claude": "Claude 3.7 Sonnet",
    "deepseek-v3": "DeepSeek-V3",
    "deepseek-v3-2503": "DeepSeek-V3-2503",
    "deepseek-r1": "DeepSeek-R1",
    "o1-mini": "o1-mini",
    "o3-mini": "o3-mini",
}

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


colors = sns.color_palette("colorblind")

blind_blue = "b"
blind_red = "r"

# blind_blue = colors[0]
# blind_red = colors[3]

correct_marker = "o"
wrong_marker = "x"

blind_green = colors[2]


def plot_tokens():
    for problem_idx in [0, 1, 8, 9, 11, 12, 15, 16, 19, 22, 23, 24]:
        # if problem_idx not in [16]:
        #     continue
        problem = PROBLEMS[problem_idx]
        levels = list(PROBLEM_LEVELS[problem])

        fig, axes = plt.subplots(nrows=4, ncols=5, figsize=(6 * 5, 3 * 4))
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
                            correct_prompt[-1].append(
                                nppc_result[seed][i][j][0]["prompt"]
                            )
                            correct_completion[-1].append(
                                nppc_result[seed][i][j][0]["completion"]
                            )
                        else:
                            wrong_prompt[-1].append(
                                nppc_result[seed][i][j][0]["prompt"]
                            )
                            wrong_completion[-1].append(
                                nppc_result[seed][i][j][0]["completion"]
                            )

            # axes[1].xlim(0, len(levels)+1)
            # axes[1].ylim(0, 10)

            r_idx = m_idx // 5
            c_idx = m_idx % 5

            all_prompts = []
            for i in range(len(levels)):
                axes[r_idx * 2][c_idx].scatter(
                    [i + 1] * len(correct_prompt[i]),
                    correct_prompt[i],
                    marker=correct_marker,
                    color=blind_blue,
                    alpha=0.15,
                    s=64,
                    # facecolor="None",
                    label="correct" if i == 0 else None,
                )

                axes[r_idx * 2][c_idx].scatter(
                    [i + 1] * len(wrong_prompt[i]),
                    wrong_prompt[i],
                    marker=wrong_marker,
                    color=blind_red,
                    alpha=0.15,
                    s=64,
                    # facecolor="None",
                    label="wrong" if i == 0 else None,
                )

                all_prompts.append(
                    (sum(correct_prompt[i]) + sum(wrong_prompt[i]))
                    / (len(correct_prompt[i]) + len(wrong_prompt[i]))
                )

            axes[r_idx * 2][c_idx].legend(fontsize=18, ncol=1, loc="upper left")
            axes[r_idx * 2][c_idx].grid(True, linestyle="--", alpha=0.6)
            axes[r_idx * 2][c_idx].set_xticks(levels)
            axes[r_idx * 2][c_idx].set_xticklabels([])
            # if m_idx != 0:
            #     axes[0][m_idx].set_yticklabels([])

            # axes[0][m_idx].set_xticks(fontsize=32)
            # axes[0][m_idx].set_yticks(fontsize=32)
            axes[r_idx * 2][c_idx].set_title(f"{MODEL2FIG[model]}", fontsize=24)
            axes[r_idx * 2][c_idx].tick_params(
                axis="both", which="major", labelsize=24
            )  # Set font size to 14 for top row

            axes[r_idx * 2][c_idx].plot(
                [i + 1 for i in range(len(all_prompts))],
                all_prompts,
                color=blind_green,
                linewidth=4.5,
                alpha=0.75,
            )

            all_completions = []
            for i in range(len(levels)):
                axes[r_idx * 2 + 1][c_idx].scatter(
                    [i + 1] * len(correct_completion[i]),
                    correct_completion[i],
                    marker=correct_marker,
                    color=blind_blue,
                    # facecolor="None",
                    s=64,
                    alpha=0.15
                    # label='correct' if i == 0 else None
                )

                axes[r_idx * 2 + 1][c_idx].scatter(
                    [i + 1] * len(wrong_completion[i]),
                    wrong_completion[i],
                    marker=wrong_marker,
                    color=blind_red,
                    s=64,
                    alpha=0.15
                    # facecolor="None",
                    # label='correct' if i == 0 else None
                )

                all_completions.append(
                    (sum(correct_completion[i]) + sum(wrong_completion[i]))
                    / (len(correct_completion[i]) + len(wrong_completion[i]))
                )

            # axes[1][m_idx].legend(fontsize=18, ncol=1, loc="upper left")
            axes[r_idx * 2 + 1][c_idx].grid(True, linestyle="--", alpha=0.6)
            axes[r_idx * 2 + 1][c_idx].set_xticks(levels)
            # axes[r_idx * 2 + 1][c_idx].set_xticklabels([])

            # if m_idx != 0:
            #     axes[1][m_idx].set_yticklabels([])

            # axes[1][m_idx].set_yticks(fontsize=32)
            axes[r_idx * 2 + 1][c_idx].tick_params(
                axis="both", which="major", labelsize=24
            )
            axes[r_idx * 2 + 1][c_idx].plot(
                [i + 1 for i in range(len(all_completions))],
                all_completions,
                color=blind_green,
                linewidth=4.5,
                alpha=0.75,
            )
        plt.subplots_adjust(hspace=0.25)
        plt.tight_layout()

        # plt.ylabel("Performance", fontsize=32)
        # plt.title("Model Performance Over Time", fontsize=24, weight="bold")
        fig_folder = "./plottings/tokens"
        file_name = fig_folder + "/tokens_{}.pdf".format(problem)
        plt.savefig(file_name, format="pdf", bbox_inches="tight")

        plt.show()


def plot_token_table():
    for m_idx, model in enumerate(model_list):
        token_prompt = []
        token_completion = []
        for problem_idx in [0, 1, 8, 9, 11, 12, 15, 16, 19, 22, 23, 24]:
            problem = PROBLEMS[problem_idx]
            levels = list(PROBLEM_LEVELS[problem])

            nppc_result = get_data_with_try(problem, levels, model)

            token_prompt_problem = []
            token_completion_problem = []
            for i in range(len(levels)):
                for seed in [42, 53, 64]:
                    if i >= len(nppc_result[seed]):
                        continue
                    for j in range(len(nppc_result[seed][i])):
                        token_prompt_problem.append(
                            nppc_result[seed][i][j][0]["prompt"]
                        )
                        token_completion_problem.append(
                            nppc_result[seed][i][j][0]["completion"]
                        )
            token_prompt.append(sum(token_prompt_problem))
            token_completion.append(sum(token_completion_problem))

        print(model, "&", sum(token_prompt), "&", sum(token_completion), "\\\\\n")


plot_tokens()
plot_token_table()
