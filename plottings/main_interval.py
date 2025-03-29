import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from npeval import plot_utils
from npeval.interval import get_interval_estimates
from npeval.metrics import MEAN, MEDIAN, IQM, OG
from npgym import PROBLEMS, PROBLEM_LEVELS
import pickle
from get_data import get_data_with_try


model_list = [
    # "qwq-32b",
    # "deepseek-r1-32b",
    "gpt-4o-mini",
    "gpt-4o",
    "claude",
    "deepseek-v3",
    "deepseek-r1",
]

fig_folder = "./performance_interval"


def save_fig(fig, name):
    file_name = fig_folder + "/{}.pdf".format(name)
    fig.savefig(file_name, format="pdf", bbox_inches="tight")
    return file_name


#
#
# save_fig(fig, "nppc_interval")
# plt.show()

aggregate_func = lambda x: np.array([MEDIAN(x), IQM(x), MEAN(x), OG(x)])


def plot_interval_per_problem():
    for problem_idx in [0, 1, 8, 9, 11, 12, 15, 16, 19, 22, 23, 24]:
        # if problem_idx not in [16]:
        #     continue
        problem = PROBLEMS[problem_idx]
        levels = list(PROBLEM_LEVELS[problem])

        nppc_result = {
            model: get_data_with_try(problem, levels, model).reshape(3, -1)
            for model in model_list
        }

        aggregate_scores, aggregate_interval_estimates = get_interval_estimates(
            nppc_result, aggregate_func, reps=50000
        )

        colors = sns.color_palette("colorblind")
        xlabels = list(nppc_result.keys())
        color_idxs = [0, 3, 4, 2, 1, 7, 8]
        nppc_colors = dict(zip(xlabels, [colors[idx] for idx in color_idxs]))

        fig, axes = plot_utils.plot_interval_estimates(
            aggregate_scores,
            aggregate_interval_estimates,
            metric_names=["Median", "IQM", "Mean", "Optimality Gap"],
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
            model: get_data_with_try(problem, levels, model).reshape(3, -1)
            for model in model_list
        }

        all_nppc_result[problem_idx] = nppc_result
    all_nppc_result_vector = {}

    for model in model_list:
        for problem_idx in [0, 1, 8, 9, 11, 12, 15, 16, 19, 22, 23, 24]:
            if model in all_nppc_result_vector:
                all_nppc_result_vector[model].append(
                    all_nppc_result[problem_idx][model]
                )
            else:
                all_nppc_result_vector[model] = [all_nppc_result[problem_idx][model]]
    for model in model_list:
        all_nppc_result_vector[model] = np.hstack(all_nppc_result_vector[model])
    aggregate_scores, aggregate_interval_estimates = get_interval_estimates(
        all_nppc_result_vector, aggregate_func, reps=50000
    )

    colors = sns.color_palette("colorblind")
    xlabels = list(all_nppc_result_vector.keys())
    color_idxs = [0, 3, 4, 2, 1, 7, 8]
    nppc_colors = dict(zip(xlabels, [colors[idx] for idx in color_idxs]))

    fig, axes = plot_utils.plot_interval_estimates(
        aggregate_scores,
        aggregate_interval_estimates,
        metric_names=["Median", "IQM", "Mean", "Optimality Gap"],
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
