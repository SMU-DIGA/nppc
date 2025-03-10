import collections

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

num_runs = 5
num_tasks = 20

nppc_result = {
    "gpt-4o": np.random.rand(num_runs, num_tasks),
    "gpt-4o-mini": np.random.rand(num_runs, num_tasks),
    "claude": np.random.rand(num_runs, num_tasks),
    "deepseek": np.random.rand(num_runs, num_tasks),
    "o1": np.random.rand(num_runs, num_tasks),
}


def subsample_scores_mat(score_mat, num_samples=5, replace=False):
    total_samples, num_games = score_mat.shape
    subsampled_scores = np.empty((num_samples, num_games))
    for i in range(num_games):
        indices = np.random.choice(total_samples, size=num_samples, replace=replace)
        subsampled_scores[:, i] = score_mat[indices, i]
    return subsampled_scores


def get_rank_matrix(score_dict, n=100000, algorithms=None):
    arr = []
    if algorithms is None:
        algorithms = sorted(score_dict.keys())
    print(f"Using algorithms: {algorithms}")
    for alg in algorithms:
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


print(get_rank_matrix(nppc_result).shape)

keys = list(nppc_result.keys())
labels = list(range(1, len(keys) + 1))
width = 1.0  # the width of the bars: can also be len(x) sequence
colors = sns.color_palette("colorblind")

fig, axes = plt.subplots(nrows=1, ncols=6, figsize=(14, 3.5))
all_ranks = get_rank_matrix(nppc_result)
for task in range(6):
    bottom = np.zeros([len(keys)])
    ax = None
    for i, key in enumerate(keys):
        ranks = all_ranks[task]
        ax = axes[task]
        ax.bar(labels, ranks[i], width, color=colors[i], bottom=bottom, alpha=0.9)
        bottom += ranks[i]

    if task == 0:
        ax.set_ylabel("Distribution", size="x-large")
    ax.set_xlabel("Ranking", size="x-large")
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

fake_patches = [mpatches.Patch(color=colors[i], alpha=0.75) for i in range(len(keys))]
legend = fig.legend(
    fake_patches,
    keys,
    loc="upper center",
    fancybox=True,
    ncol=len(keys),
    fontsize="x-large",
)
fig.subplots_adjust(top=0.78, wspace=0.1, hspace=0.05)
plt.show()
