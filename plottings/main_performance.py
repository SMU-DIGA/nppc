import matplotlib.pyplot as plt
import numpy as np

from npeval import metrics
from npeval import plot_utils
from npeval.interval import get_interval_estimates
import pickle

import os.path as osp
from pathlib import Path

from npgym import PROBLEMS, PROBLEM_LEVELS


def get_data(problem, levels, model):
    # print(model)
    seeds = [42, 53, 64]
    results = []
    for seed in seeds:
        seed_result = []
        # print("========")
        # print("seed: {}".format(seed))
        # print("========")
        for level in levels:
            f = open(
                "../results/{}/{}/model_{}_problem_{}_level_{}_shots_1_seed_{}.pkl".format(
                    problem, model, model, problem, level, seed
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
            seed_result.append(true_num / 30)
        # print(seed_result)
        results.append(seed_result)
    results = np.array(results).reshape(3, 1, len(levels))
    return results


problem_idx = 0

problem = PROBLEMS[0]
levels = list(PROBLEM_LEVELS[problem])

model_list = ["deepseek-v3", "deepseek-r1", "claude", "gpt-4o", "gpt-4o-mini"]
nppc_result = {}

for model in model_list:
    nppc_result[model] = get_data(problem, levels, model)

ale_all_frames_scores_dict = nppc_result
frames = np.array(levels) - 1
ale_frames_scores_dict = {
    algorithm: score[:, :, frames]
    for algorithm, score in ale_all_frames_scores_dict.items()
}
iqm = lambda scores: np.array(
    [metrics.aggregate_iqm(scores[..., frame]) for frame in range(scores.shape[-1])]
)
iqm_scores, iqm_cis = get_interval_estimates(ale_frames_scores_dict, iqm, reps=2000)

fig, ax = plt.subplots(figsize=(7, 5))

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
    legend=True
    # xticklabels = x_ticks,
    # yticklables = y_ticks
)

plt.tight_layout()

plots_folder = "./performance_over_levels"
path_plots_folder = Path(plots_folder)
if not path_plots_folder.exists():
    path_plots_folder.mkdir(parents=True, exist_ok=True)
plt.savefig(
    osp.join(plots_folder, "{}.pdf".format(problem)),
    bbox_inches="tight",
    pad_inches=0.0,
)
plt.show()
