import matplotlib.pyplot as plt
import numpy as np

from npeval import metrics
from npeval import plot_utils
from npeval.interval import get_interval_estimates
import pickle

def get_data(problem, levels, model):
    seeds = [42, 53, 64]
    results = []
    for seed in seeds:
        seed_result = []
        # print("========")
        # print("seed: {}".format(seed))
        # print("========")
        for level in levels:
            f = open(
                "../results/{}/{}/model_{}_problem_{}_level_{}_shots_1_seed_{}.pkl".format(problem, model, model, problem, level, seed),
                'rb')
            data = pickle.load(f)
            true_num = 0
            for i in range(30):
                if data[level][i]["correctness"] == True:
                    true_num = true_num + 1
            # print("level {}, accuracy = {}".format(level, true_num / 30))
            seed_result.append(true_num / 30)
        # print(seed_result)
        results.append(seed_result)
    results = np.array(results).reshape(3, 1, len(levels))
    return  results


# num_runs = 3
# num_tasks = 1
# num_frames = 11
#
# nppc_result = {
#     "gpt-4o": np.random.rand(num_runs, num_tasks, num_frames),
#     "gpt-4o-mini": np.random.rand(num_runs, num_tasks, num_frames),
#     "claude": np.random.rand(num_runs, num_tasks, num_frames),
#     "deepseek": np.random.rand(num_runs, num_tasks, num_frames),
#     "o1": np.random.rand(num_runs, num_tasks, num_frames),
# }

problem = "3-Satisfiability (3-SAT)"
levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

model = "deepseek-v3"
deepseek_v3 = get_data(problem, levels, model)
print(deepseek_v3)
model = "deepseek-r1"
deepseek_r1 = get_data(problem, levels, model)
print(deepseek_r1)


nppc_result = {
    "deepseek-v3": deepseek_v3,
    "deepseek-r1": deepseek_r1,
}


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
plot_utils.plot_sample_efficiency_curve(
    frames + 1,
    iqm_scores,
    iqm_cis,
    algorithms=list(nppc_result.keys()),
    xlabel=r"Difficulty Level",
    ylabel="Accuracy",
    ax=ax,
)

# 获取所有线条和算法名称
lines = ax.get_lines()
algorithms = list(nppc_result.keys())

# 为每条线设置标签
for line, algo in zip(lines, algorithms):
    line.set_label(algo)  # 设置标签

# 添加图例
ax.legend(
    bbox_to_anchor=(1.05, 1),  # 避免遮挡主图
    # loc="upper left"
)

plt.tight_layout()
plt.savefig("{}.png".format(problem))
plt.show()

