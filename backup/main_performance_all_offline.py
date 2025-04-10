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
                true_num = 0
                for i in range(30):
                    # if model == 'gpt-4o':
                    #     print(data[level][i]["instance"])
                    if data[level][i]["correctness"]:
                        true_num = true_num + 1
                # print("level {}, accuracy = {}".format(level, true_num / 30))
                results[seed].append(true_num / 30)
            except:
                min_len = min(min_len, len(results[seed]))
                break
        # print(seed_result)
    if min_len > 0:
        results = np.array([results[seed][:min_len] for seed in seeds]).reshape(
            3, 1, min_len
        )
        return results

    return None


# def get_data(problem, levels, model):
#     # print(model)
#     seeds = [42, 53, 64]
#     results = []
#
#     model_to_file = {
#         "qwq-32b": "qwq",
#         "deepseek-r1-32b": "deepseek-r1-32",
#         "gpt-4o-mini": "gpt-4o-mini",
#         "gpt-4o": "gpt-4o",
#         "claude": "claude",
#         "deepseek-v3": "deepseek-v3",
#         "deepseek-r1": "deepseek-r1",
#     }
#
#     for seed in seeds:
#         seed_result = []
#         # print("========")
#         # print("seed: {}".format(seed))
#         # print("========")
#         if model in ["deepseek-r1"]:
#             result_file_template = (
#                 "../results_r1/{}/{}/model_{}_problem_{}_level_{}_shots_1_seed_{}.pkl"
#             )
#         else:
#             result_file_template = (
#                 "../results/{}/{}/model_{}_problem_{}_level_{}_shots_1_seed_{}.pkl"
#             )
#         for level in levels:
#             f = open(
#                 result_file_template.format(
#                     problem,
#                     model_to_file[model],
#                     model_to_file[model],
#                     problem,
#                     level,
#                     seed,
#                 ),
#                 "rb",
#             )
#             data = pickle.load(f)
#             true_num = 0
#             for i in range(30):
#                 # if model == 'gpt-4o':
#                 #     print(data[level][i]["instance"])
#                 if data[level][i]["correctness"]:
#                     true_num = true_num + 1
#             # print("level {}, accuracy = {}".format(level, true_num / 30))
#             seed_result.append(true_num / 30)
#         # print(seed_result)
#         results.append(seed_result)
#     results = np.array(results).reshape(3, 1, len(levels))
#     return results


model_list = [
    "qwq-32b",
    "deepseek-r1-32b",
    "gpt-4o-mini",
    "gpt-4o",
    "claude",
    "deepseek-v3",
    "deepseek-r1",
    "o1-mini",
]

color_palette = "colorblind"
color_palette = sns.color_palette(color_palette, n_colors=len(model_list))
colors = dict(zip([model_list[i] for i in [6, 5, 4, 1, 3, 0, 2, 7]], color_palette))


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
        algorithms=list(nppc_result.keys()),
        xlabel=r"Difficulty Level",
        ylabel="Accuracy",
        ax=ax,
        xticks=x_ticks,
        yticks=y_ticks,
        legend=True,
        colors=colors
        # xticklabels = x_ticks,
        # yticklables = y_ticks
    )


problem_idx = 19

for problem_idx in [0, 1, 8, 9, 11, 12, 15, 16, 19, 22, 23, 24]:
    # if problem_idx not in [16]:
    #     continue
    problem = PROBLEMS[problem_idx]
    levels = list(PROBLEM_LEVELS[problem])

    # if problem_idx == 9:
    #     levels = levels[:9]
    fig, ax = plt.subplots(figsize=(7, 5))

    for model in model_list[:2]:
        plot_one_line(ax=ax, model=model, colors=colors, levels=levels, problem=problem)
    # ax.set_xscale('log')
    plt.tight_layout()

    plots_folder = "./performance_over_levels_offline"
    path_plots_folder = Path(plots_folder)
    if not path_plots_folder.exists():
        path_plots_folder.mkdir(parents=True, exist_ok=True)
    plt.savefig(
        osp.join(plots_folder, "{}.pdf".format(problem)),
        bbox_inches="tight",
        pad_inches=0.0,
    )
    plt.show()
