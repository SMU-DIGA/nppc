from npeval import metrics
import numpy as np
from npeval.interval import get_interval_estimates
from npeval import plot_utils
import seaborn as sns
import matplotlib.pyplot as plt

num_runs = 5
num_tasks = 20

nppc_result = {
    "gpt-4o": np.random.rand(num_runs, num_tasks),
    "gpt-4o-mini": np.random.rand(num_runs, num_tasks),
    "claude": np.random.rand(num_runs, num_tasks),
    "deepseek": np.random.rand(num_runs, num_tasks),
    "o1": np.random.rand(num_runs, num_tasks),
}

print(nppc_result)

IQM = lambda x: metrics.aggregate_iqm(x)  # Interquartile Mean
OG = lambda x: metrics.aggregate_optimality_gap(x, 1.0)  # Optimality Gap
MEAN = lambda x: metrics.aggregate_mean(x)
MEDIAN = lambda x: metrics.aggregate_median(x)
aggregate_func = lambda x: np.array([MEDIAN(x), IQM(x), MEAN(x), OG(x)])

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


def save_fig(fig, name):
    file_name = "{}.pdf".format(name)
    fig.savefig(file_name, format="pdf", bbox_inches="tight")
    return file_name


save_fig(fig, "nppc_interval")
plt.show()
