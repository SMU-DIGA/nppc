import collections

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from npgym import PROBLEMS, PROBLEM_LEVELS
from get_data import get_data_with_try
from npeval import plot_utils

fig_folder = "./performance_rank"


def save_fig(fig, name):
    file_name = fig_folder + "/{}.pdf".format(name)
    fig.savefig(file_name, format="pdf", bbox_inches="tight")
    return file_name


def subsample_scores_mat(score_mat, num_samples=5, replace=False):
    total_samples, num_games = score_mat.shape
    subsampled_scores = np.empty((num_samples, num_games))
    for i in range(num_games):
        indices = np.random.choice(total_samples, size=num_samples, replace=replace)
        subsampled_scores[:, i] = score_mat[indices, i]
    print(subsampled_scores.shape)
    return subsampled_scores


def get_rank_matrix(score_dict, n=100000, algorithms=None):
    arr = []
    if algorithms is None:
        algorithms = sorted(score_dict.keys())
    print(f"Using algorithms: {algorithms}")
    for alg in algorithms:
        # print(alg)
        arr.append(subsample_scores_mat(score_dict[alg], num_samples=n, replace=True))
    X = np.stack(arr, axis=0)
    num_algs, _, num_tasks = X.shape
    all_mat = []
    for task in range(num_tasks):
        # Sort based on negative scores as rank 0 corresponds to minimum value,
        # rank 1 corresponds to second minimum value when using lexsort.
        task_x = -X[:, :, task]
        # This is done to randomly break ties.
        rand_x = np.random.random(size=task_x.shape)
        # Last key is the primary key,
        indices = np.lexsort((rand_x, task_x), axis=0)
        mat = np.zeros((num_algs, num_algs))
        for rank in range(num_algs):
            cnts = collections.Counter(indices[rank])
            mat[:, rank] = np.array([cnts[i] / n for i in range(num_algs)])
        all_mat.append(mat)
    all_mat = np.stack(all_mat, axis=0)
    return all_mat


model_list = [
    # "qwq-32b",
    # "deepseek-r1-32b",
    "gpt-4o-mini",
    "gpt-4o",
    "claude",
    "deepseek-v3",
    "deepseek-r1",
]


def plot_rank_per_problem():
    fig, axes = plt.subplots(nrows=2, ncols=6, figsize=(3.5 * 6, 3.5 * 2))
    colors = sns.color_palette("colorblind")
    for p_idx, problem_idx in enumerate([0, 1, 8, 9, 11, 12, 15, 16, 19, 22, 23, 24]):
        # if problem_idx not in [16]:
        #     continue

        ax = axes[p_idx // 6][p_idx % 6]

        problem = PROBLEMS[problem_idx]
        levels = list(PROBLEM_LEVELS[problem])

        nppc_result = {
            model: get_data_with_try(problem, levels, model).reshape(3, -1)
            for model in model_list
        }
        keys = list(nppc_result.keys())
        labels = list(range(1, len(keys) + 1))
        width = 1.0  # the width of the bars: can also be len(x) sequence

        # fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 3.5))
        all_ranks = get_rank_matrix(nppc_result, algorithms=model_list)

        mean_ranks = np.mean(all_ranks, axis=0)
        print(mean_ranks)

        bottom = np.zeros([len(keys)])
        # fig, ax = plt.subplots()
        for i, key in enumerate(keys):
            # ranks = all_ranks[task]
            ax.bar(
                labels,
                mean_ranks[i],
                width,
                color=colors[i],
                bottom=bottom,
                alpha=0.9,
                edgecolor="white",
                linewidth=1.5,
            )
            bottom += mean_ranks[i]

        if p_idx % 6 == 0:
            ax.set_ylabel("Distribution", size="x-large")
        ax.set_xlabel("{}".format(problem), size="x-large")
        ax.set_xticks(labels)
        ax.set_ylim(0, 1)
        ax.set_xticklabels(labels, size="large")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.tick_params(
            axis="both",
            which="both",
            bottom=False,
            top=False,
            left=False,
            right=False,
            labeltop=False,
            labelbottom=True,
            labelleft=False,
            labelright=False,
        )

    fake_patches = [
        mpatches.Patch(color=colors[i], alpha=0.75) for i in range(len(model_list))
    ]
    legend = fig.legend(
        fake_patches,
        model_list,
        loc="upper center",
        fancybox=True,
        ncol=len(model_list),
        fontsize="x-large",
    )

    save_fig(fig, "rank_all")
    # fig.subplots_adjust(top=0.78, wspace=0.1, hspace=0.05)
    # fig.savefig("test.png", bbox_inches="tight", dpi=300)


# def plot_rank_all_problems():
#     all_nppc_result = {}
#     for problem_idx in [0, 1, 8, 9, 11, 12, 15, 16, 19, 22, 23, 24]:
#         # if problem_idx not in [16]:
#         #     continue
#         problem = PROBLEMS[problem_idx]
#         levels = list(PROBLEM_LEVELS[problem])
#
#         nppc_result = {
#             model: get_data_with_try(problem, levels, model).reshape(3, -1)
#             for model in model_list
#         }
#
#         all_nppc_result[problem_idx] = nppc_result
#     all_nppc_result_vector = {}
#
#     for model in model_list:
#         for problem_idx in [0, 1, 8, 9, 11, 12, 15, 16, 19, 22, 23, 24]:
#             if model in all_nppc_result_vector:
#                 all_nppc_result_vector[model].append(all_nppc_result[problem_idx][model])
#             else:
#                 all_nppc_result_vector[model] = [all_nppc_result[problem_idx][model]]
#     for model in model_list:
#         all_nppc_result_vector[model] = np.hstack(all_nppc_result_vector[model])
#     aggregate_scores, aggregate_interval_estimates = get_interval_estimates(
#         all_nppc_result_vector, aggregate_func, reps=50000
#     )
#
#     colors = sns.color_palette("colorblind")
#     xlabels = list(all_nppc_result_vector.keys())
#     color_idxs = [0, 3, 4, 2, 1, 7, 8]
#     nppc_colors = dict(zip(xlabels, [colors[idx] for idx in color_idxs]))
#
#     fig, axes = plot_utils.plot_interval_estimates(
#         aggregate_scores,
#         aggregate_interval_estimates,
#         metric_names=["Median", "IQM", "Mean", "Optimality Gap"],
#         algorithms=xlabels,
#         colors=nppc_colors,
#         xlabel_y_coordinate=-0.16,
#         xlabel="",
#     )
#     save_fig(fig, "interval_all")
#     plt.show()

plot_rank_per_problem()

# import collections
#
# import matplotlib.patches as mpatches
# import matplotlib.pyplot as plt
# import numpy as np
# import seaborn as sns
#
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
#
# def subsample_scores_mat(score_mat, num_samples=5, replace=False):
#     total_samples, num_games = score_mat.shape
#     subsampled_scores = np.empty((num_samples, num_games))
#     for i in range(num_games):
#         indices = np.random.choice(total_samples, size=num_samples, replace=replace)
#         subsampled_scores[:, i] = score_mat[indices, i]
#     return subsampled_scores
#
#
# def get_rank_matrix(score_dict, n=100000, algorithms=None):
#     arr = []
#     if algorithms is None:
#         algorithms = sorted(score_dict.keys())
#     print(f"Using algorithms: {algorithms}")
#     for alg in algorithms:
#         arr.append(subsample_scores_mat(score_dict[alg], num_samples=n, replace=True))
#     X = np.stack(arr, axis=0)
#     num_algs, _, num_tasks = X.shape
#     all_mat = []
#     for task in range(num_tasks):
#         # Sort based on negative scores as rank 0 corresponds to minimum value,
#         # rank 1 corresponds to second minimum value when using lexsort.
#         task_x = -X[:, :, task]
#         # This is done to randomly break ties.
#         rand_x = np.random.random(size=task_x.shape)
#         # Last key is the primary key,
#         indices = np.lexsort((rand_x, task_x), axis=0)
#         mat = np.zeros((num_algs, num_algs))
#         for rank in range(num_algs):
#             cnts = collections.Counter(indices[rank])
#             mat[:, rank] = np.array([cnts[i] / n for i in range(num_algs)])
#         all_mat.append(mat)
#     all_mat = np.stack(all_mat, axis=0)
#     return all_mat
#
#
# print(get_rank_matrix(nppc_result).shape)
#
# keys = list(nppc_result.keys())
# labels = list(range(1, len(keys) + 1))
# width = 1.0  # the width of the bars: can also be len(x) sequence
# colors = sns.color_palette("colorblind")
#
# fig, axes = plt.subplots(nrows=1, ncols=6, figsize=(14, 3.5))
# all_ranks = get_rank_matrix(nppc_result)
# for task in range(6):
#     bottom = np.zeros([len(keys)])
#     ax = None
#     for i, key in enumerate(keys):
#         ranks = all_ranks[task]
#         ax = axes[task]
#         ax.bar(labels, ranks[i], width, color=colors[i], bottom=bottom, alpha=0.9)
#         bottom += ranks[i]
#
#     if task == 0:
#         ax.set_ylabel("Distribution", size="x-large")
#     ax.set_xlabel("Ranking", size="x-large")
#     ax.set_xticks(labels)
#     ax.set_ylim(0, 1)
#     ax.set_xticklabels(labels, size="large")
#     ax.spines["top"].set_visible(False)
#     ax.spines["right"].set_visible(False)
#     ax.spines["bottom"].set_visible(False)
#     ax.spines["left"].set_visible(False)
#     ax.tick_params(
#         axis="both",
#         which="both",
#         bottom=False,
#         top=False,
#         left=False,
#         right=False,
#         labeltop=False,
#         labelbottom=True,
#         labelleft=False,
#         labelright=False,
#     )
#
# fake_patches = [mpatches.Patch(color=colors[i], alpha=0.75) for i in range(len(keys))]
# legend = fig.legend(
#     fake_patches,
#     keys,
#     loc="upper center",
#     fancybox=True,
#     ncol=len(keys),
#     fontsize="x-large",
# )
# fig.subplots_adjust(top=0.78, wspace=0.1, hspace=0.05)
# fig.savefig("test.png", bbox_inches="tight", dpi=300)

#
# keys = algs
# labels = list(range(1, len(keys) + 1))
# width = 1.0  # the width of the bars: can also be len(x) sequence
#
# # fig, axes = plt.subplots(ncols=2, figsize=(2.9 * 2, 3.6))
# fig, axes = plt.subplots(nrows=2, figsize=(2, 2.3 * 2))
#
# for main_idx, main_key in enumerate(['100k', '500k']):
#     ax = axes[main_idx]
#     mean_ranks = mean_ranks_all[main_key]
#     bottom = np.zeros_like(mean_ranks[0])
#     for i, key in enumerate(algs):
#         label = key if main_idx == 0 else None
#         ax.bar(labels, mean_ranks[i], width, label=label,
#                color=DMC_COLOR_DICT[key], bottom=bottom, alpha=0.9)
#         bottom += mean_ranks[i]
#
#     yticks = np.array(range(0, 101, 20))
#     ax.set_yticklabels(yticks, size='large')
#     # if main_idx == 0:
#     #   ax.set_ylabel('Fraction (in %)', size='x-large')
#     #   yticks = np.array(range(0, 101, 20))
#     #   ax.set_yticklabels(yticks, size='large')
#     # else:
#     #   ax.set_yticklabels([])
#
#     ax.set_yticks(yticks * 0.01)
#     # ax.set_xlabel('Ranking', size='x-large')
#     if main_idx != 0:
#         ax.set_xticks(labels)
#     else:
#         ax.set_xticks([])
#     ax.set_xticklabels(labels, size='large')
#     ax.set_title(main_key + ' steps', size='x-large', y=0.95)
#     ax.spines['top'].set_visible(False)
#     ax.spines['right'].set_visible(False)
#     ax.spines['bottom'].set_visible(False)
#     ax.spines['left'].set_visible(False)
#     # left = True if main_idx == 0 else False
#     left = True
#     ax.tick_params(axis='both', which='both', bottom=False, top=False,
#                    left=left, right=False, labeltop=False,
#                    labelbottom=True, labelleft=left, labelright=False)
#
# fig.legend(loc='center right', fancybox=True, ncol=1, fontsize='x-large', bbox_to_anchor=(2.05, 0.40))
# fig.subplots_adjust(top=0.72, wspace=0.0, bottom=0)
# fig.text(x=-0.2, y=0.2, s='Fraction (in %)', rotation=90, size='xx-large')
# plt.show()
