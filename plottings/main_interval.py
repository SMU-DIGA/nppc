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
from npsolver.solver import (
    extract_solution_from_response,
    extract_solution_from_response_old,
)
import seaborn as sns
import matplotlib.lines as mlines

from npeval import plot_utils
from npeval.interval import get_interval_estimates
from npeval.metrics import MEAN, MEDIAN, IQM, OG
from npgym import PROBLEMS, PROBLEM_LEVELS
import pickle


# from get_data import get_data_with_try


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
        "deepseek-v3-2503": "deepseek-v3-2503",
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
                # correctness = []
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
                # print(verify_results)
                verify_results = [res[0] for res in verify_results]
                # print("level {}, accuracy = {}".format(level, true_num / 30))
                results[seed].append(
                    np.sum(np.array(verify_results)) / len(verify_results)
                )
            except:
                min_len = min(min_len, len(results[seed]))
                continue
    if min_len > 0:
        results = np.array([results[seed][:min_len] for seed in seeds]).reshape(
            3, 1, min_len
        )
        return results

    return None


fig_folder = "./plottings/performance_interval"

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


def save_fig(fig, name):
    file_name = fig_folder + "/{}.pdf".format(name)
    fig.savefig(file_name, format="pdf", bbox_inches="tight")
    return file_name


#
#
# save_fig(fig, "nppc_interval")
# plt.show()

aggregate_func = lambda x: np.array([IQM(x), MEAN(x), MEDIAN(x), OG(x)])


def plot_interval_per_problem():
    for problem_idx in [0, 1, 8, 9, 11, 12, 15, 16, 19, 22, 23, 24]:
        # if problem_idx not in [16]:
        #     continue
        problem = PROBLEMS[problem_idx]
        levels = list(PROBLEM_LEVELS[problem])

        nppc_result = {
            MODEL2FIG[model]: get_data_with_try(problem, levels, model).reshape(3, -1)
            for model in model_list
        }

        aggregate_scores, aggregate_interval_estimates = get_interval_estimates(
            nppc_result, aggregate_func, reps=50000
        )

        colors = sns.color_palette("colorblind")
        xlabels = list(nppc_result.keys())
        color_palette = "colorblind"
        color_palette = sns.color_palette(color_palette, n_colors=len(model_list))
        nppc_colors = dict(
            zip(
                [MODEL2FIG[model_list[i]] for i in range(len(model_list))],
                color_palette,
            )
        )

        fig, axes = plot_utils.plot_interval_estimates(
            aggregate_scores,
            aggregate_interval_estimates,
            metric_names=["IQM", "Mean", "Median", "Optimality Gap"],
            algorithms=xlabels,
            colors=nppc_colors,
            xlabel_y_coordinate=-0.16,
            xlabel="",
        )

        save_fig(fig, "interval_{}".format(problem))

        plt.show()


def plot_interval_all_problems():
    all_nppc_result = {}
    for problem_idx in [0, 1, 8, 9, 11, 12, 15, 16, 19, 22, 23, 24]:
        # if problem_idx not in [16]:
        #     continue
        problem = PROBLEMS[problem_idx]
        levels = list(PROBLEM_LEVELS[problem])

        nppc_result = {
            MODEL2FIG[model]: get_data_with_try(problem, levels, model).reshape(3, -1)
            for model in model_list
        }

        all_nppc_result[problem_idx] = nppc_result
    all_nppc_result_vector = {}

    for model in model_list:
        for problem_idx in [0, 1, 8, 9, 11, 12, 15, 16, 19, 22, 23, 24]:
            if MODEL2FIG[model] in all_nppc_result_vector:
                all_nppc_result_vector[MODEL2FIG[model]].append(
                    all_nppc_result[problem_idx][MODEL2FIG[model]]
                )
            else:
                all_nppc_result_vector[MODEL2FIG[model]] = [
                    all_nppc_result[problem_idx][MODEL2FIG[model]]
                ]
    for model in model_list:
        all_nppc_result_vector[MODEL2FIG[model]] = np.hstack(
            all_nppc_result_vector[MODEL2FIG[model]]
        )
    aggregate_scores, aggregate_interval_estimates = get_interval_estimates(
        all_nppc_result_vector, aggregate_func, reps=50000
    )

    colors = sns.color_palette("colorblind")
    xlabels = list(all_nppc_result_vector.keys())
    # color_idxs = [0, 3, 4, 2, 1, 7, 8]
    # nppc_colors = dict(zip(xlabels, [colors[idx] for idx in color_idxs]))

    color_palette = "colorblind"
    color_palette = sns.color_palette(color_palette, n_colors=len(model_list))
    nppc_colors = dict(
        zip([MODEL2FIG[model_list[i]] for i in range(len(model_list))], color_palette)
    )

    fig, axes = plot_utils.plot_interval_estimates(
        aggregate_scores,
        aggregate_interval_estimates,
        metric_names=["IQM", "Mean", "Median", "Optimality Gap"],
        algorithms=xlabels,
        colors=nppc_colors,
        xlabel_y_coordinate=-0.16,
        xlabel="",
    )
    save_fig(fig, "interval_all")
    plt.show()


plot_interval_per_problem()
plot_interval_all_problems()
# if problem_idx == 9:
#     levels = levels[:9]
# fig, ax = plt.subplots(figsize=(7, 5))

# num_runs = 5
# num_tasks = 20
#
# nppc_result = {
#     "gpt-4o": np.random.rand(num_runs, num_tasks),
#     "gpt-4o-mini": np.random.rand(num_runs, num_tasks),
#     "claude": np.random.rand(num_runs, num_tasks),
#     "deepseek": np.random.rand(num_runs, num_tasks),
#     "o1": np.random.rand(num_runs, num_tasks),
# }
#
# print(nppc_result)
#
# aggregate_func = lambda x: np.array([MEDIAN(x), IQM(x), MEAN(x), OG(x)])
#
# aggregate_scores, aggregate_interval_estimates = get_interval_estimates(
#     nppc_result, aggregate_func, reps=50000
# )
#
# colors = sns.color_palette("colorblind")
# xlabels = list(nppc_result.keys())
# color_idxs = [0, 3, 4, 2, 1, 7, 8]
# nppc_colors = dict(zip(xlabels, [colors[idx] for idx in color_idxs]))
#
# fig, axes = plot_utils.plot_interval_estimates(
#     aggregate_scores,
#     aggregate_interval_estimates,
#     metric_names=["Median", "IQM", "Mean", "Optimality Gap"],
#     algorithms=xlabels,
#     colors=nppc_colors,
#     xlabel_y_coordinate=-0.16,
#     xlabel="",
# )
#
#
# def save_fig(fig, name):
#     file_name = "{}.pdf".format(name)
#     fig.savefig(file_name, format="pdf", bbox_inches="tight")
#     return file_name
#
#
# save_fig(fig, "nppc_interval")
# plt.show()
