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
        "deepseek-v3-2503": "deepseek-v3-2503",
        "o3-mini": "o3-mini",
    }

    env = NPEnv(problem_name=problem, level=1)

    for seed in seeds:
        results[seed] = []

        for level in levels:
            try:
                if model in ["deepseek-r1", "deepseek-v3-2503", "o3-mini"]:
                    result_file_template = "./results_r1/{}/{}/model_{}_problem_{}_level_{}_shots_1_seed_{}.pkl"
                else:
                    result_file_template = "./results/{}/{}/model_{}_problem_{}_level_{}_shots_1_seed_{}.pkl"
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
                # correctness = []
                instances = []
                solutions = []
                for i in range(30):
                    # print(data[level][i])
                    # if model == 'gpt-4o':
                    #     print(data[level][i]["instance"])
                    instances.append(data[level][i]["instance"])
                    predicted_solution, _ = extract_solution_from_response(
                        data[level][i]["response"]
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


# model_list = [
#     # "qwq-32b",
#     # "deepseek-r1-32b",
#     "gpt-4o-mini",
#     "gpt-4o",
#     "claude",
#     "deepseek-v3",
#     "deepseek-r1",
#     "o1-mini",
# ]

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

color_palette = "colorblind"
color_palette = sns.color_palette(color_palette, n_colors=len(model_list))
colors = dict(zip([model_list[i] for i in range(len(model_list))], color_palette))


# model_list = ["gpt-4o-mini"]


def plot_one_line(ax, problem, model, levels, colors):
    nppc_result = {model: get_data_with_try(problem, levels, model)}

    if nppc_result[model] is None:
        return
    # print(nppc_result)
    # for model in model_list:
    #     nppc_result[model] = get_data(problem, levels, model)

    ale_all_frames_scores_dict = nppc_result
    frames = np.array(levels)[: nppc_result[model].shape[-1]] - 1
    ale_frames_scores_dict = {
        algorithm: score[:, :, frames]
        for algorithm, score in ale_all_frames_scores_dict.items()
    }
    iqm = lambda scores: np.array(
        [metrics.aggregate_iqm(scores[..., frame]) for frame in range(scores.shape[-1])]
    )
    iqm_scores, iqm_cis = get_interval_estimates(ale_frames_scores_dict, iqm, reps=2000)

    x_ticks = np.arange(1, len(frames) + 1)  # 假设frames是一个数组，表示难度级别
    # ax.set_xticks(x_ticks)
    y_ticks = np.linspace(0, 1, 6)  # 创建0到1之间的11个均匀分布的点
    # ax.set_yticks(y_ticks)
    plot_utils.plot_sample_efficiency_curve(
        frames + 1,
        iqm_scores,
        iqm_cis,
        # algorithms=list(nppc_result.keys()),
        xlabel=r"Difficulty Level",
        ylabel="Accuracy",
        ax=ax,
        xticks=x_ticks,
        yticks=y_ticks,
        legend=False,
        colors=colors,
        # xticklabels = x_ticks,
        # yticklables = y_ticks
    )


def _decorate_axis(ax, wrect=10, hrect=10, ticklabelsize="large", leftfalse=False):
    """Helper function for decorating plots."""
    # Hide the right and top spines
    # ax.spines["right"].set_visible(False)
    # ax.spines["top"].set_visible(False)
    # if leftfalse:
    #     ax.spines["left"].set_visible(False)
    # else:
    #     ax.spines["left"].set_linewidth(2)
    ax.spines["bottom"].set_linewidth(1)
    ax.spines["right"].set_linewidth(1)
    ax.spines["top"].set_linewidth(1)
    ax.spines["left"].set_linewidth(1)
    # Deal with ticks and the blank space at the origin
    ax.tick_params(length=0.1, width=0.1, labelsize=ticklabelsize)
    # ax.spines["left"].set_position(("outward", hrect))
    # ax.spines["bottom"].set_position(("outward", wrect))
    return ax


def _annotate_and_decorate_axis(
    ax,
    labelsize="x-large",
    ticklabelsize="x-large",
    xticks=None,
    xticklabels=None,
    yticks=None,
    legend=False,
    grid_alpha=0.2,
    legendsize="x-large",
    xlabel="",
    ylabel="",
    wrect=10,
    hrect=10,
):
    """Annotates and decorates the plot."""
    ax.set_xlabel(xlabel, fontsize=labelsize)
    ax.set_ylabel(ylabel, fontsize=labelsize)
    if xticks is not None:
        ax.set_xticks(ticks=xticks)
        # ax.set_xticklabels(xticklabels)
    leftfalse = False
    if yticks is not None:
        ax.set_yticks(yticks)
    else:
        ax.set_yticks([])
        leftfalse = True
    # ax.grid(True, alpha=grid_alpha)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax = _decorate_axis(
        ax, wrect=wrect, hrect=hrect, ticklabelsize=ticklabelsize, leftfalse=leftfalse
    )

    if legend:
        ax.legend(fontsize=legendsize, loc="upper right", framealpha=0.5)
    return ax


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

# MODEL2FIG = {
#     "deepseek-r1-32b": "DeepSeek-R1-32B",
#     "qwq-32b": "QwQ-32B",
#     "gpt-4o-mini": "GPT-4o-mini",
#     "gpt-4o": "GPT-4o",
#     "claude": "Claude 3.7 Sonnet",
#     "deepseek-v3": "DeepSeek-V3",
#     "deepseek-v3-2503": "DeepSeek-V3-2503",
#     "deepseek-r1": "DeepSeek-R1",
#     "o1-mini": "o1-mini",
#     "o3-mini": "o3-mini",
# }

fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(5 * 4, 3.5 * 3))
for p_idx, problem_idx in enumerate([0, 1, 8, 9, 11, 12, 15, 16, 19, 22, 23, 24]):
    # if problem_idx not in [16]:
    #     continue
    problem = PROBLEMS[problem_idx]
    levels = list(PROBLEM_LEVELS[problem])

    ax = axes[p_idx // 4][p_idx % 4]

    for model in model_list:
        nppc_result = {model: get_data_with_try(problem, levels, model)}

        if nppc_result[model] is None:
            continue
        # print(nppc_result)
        # for model in model_list:
        #     nppc_result[model] = get_data(problem, levels, model)

        ale_all_frames_scores_dict = nppc_result
        frames = np.array(levels)[: nppc_result[model].shape[-1]] - 1
        ale_frames_scores_dict = {
            algorithm: score[:, :, frames]
            for algorithm, score in ale_all_frames_scores_dict.items()
        }
        iqm = lambda scores: np.array(
            [
                metrics.aggregate_iqm(scores[..., frame])
                for frame in range(scores.shape[-1])
            ]
        )
        iqm_scores, iqm_cis = get_interval_estimates(
            ale_frames_scores_dict, iqm, reps=2000
        )

        x_ticks = np.arange(1, len(frames) + 1)  # 假设frames是一个数组，表示难度级别
        # ax.set_xticks(x_ticks)
        y_ticks = np.linspace(0, 1, 6)  # 创建0到1之间的11个均匀分布的点

        # for algorithm in algorithms:
        metric_values = iqm_scores[model]
        lower, upper = iqm_cis[model]
        ax.plot(
            frames + 1,
            metric_values,
            color=colors[model],
            # marker=kwargs.get("marker", "o"),
            linewidth=2,
            label=MODEL2FIG[model],
        )
        ax.set_title(f"{PROBLEM2FIG[problem]}", fontsize=24)
        ax.fill_between(frames + 1, y1=lower, y2=upper, color=colors[model], alpha=0.2)
        if p_idx % 4 == 0:
            _annotate_and_decorate_axis(ax, xticks=x_ticks, yticks=y_ticks)
        else:
            _annotate_and_decorate_axis(ax, xticks=x_ticks)

        ax.tick_params(axis="both", which="major", labelsize=24)

        # ax.set_yticks(y_ticks)
        # plot_utils.plot_sample_efficiency_curve(
        #     frames + 1,
        #     iqm_scores,
        #     iqm_cis,
        #     # algorithms=list(nppc_result.keys()),
        #     xlabel=r"Difficulty Level",
        #     ylabel="Accuracy",
        #     ax=ax,
        #     xticks=x_ticks,
        #     yticks=y_ticks,
        #     legend=False,
        #     colors=colors,
        #
        #     # xticklabels = x_ticks,
        #     # yticklables = y_ticks
        # )
    # ax.set_xscale('log')
fake_lines = [
    mlines.Line2D(
        [], [], color=colors[model], linestyle="-", linewidth=4, label=MODEL2FIG[model]
    )
    for model in model_list
]
fig.legend(
    handles=fake_lines,
    loc="lower center",
    bbox_to_anchor=(0.5, 1.0),
    ncol=5,
    fancybox=True,
    # shadow=True,
    fontsize=24,
)
plt.subplots_adjust(hspace=0.25)

plt.tight_layout()


plots_folder = "./plottings/performance_over_levels"
path_plots_folder = Path(plots_folder)
if not path_plots_folder.exists():
    path_plots_folder.mkdir(parents=True, exist_ok=True)
plt.savefig(
    osp.join(plots_folder, "{}.pdf".format("performance_over_levels")),
    bbox_inches="tight",
    pad_inches=0.0,
)
plt.show()
