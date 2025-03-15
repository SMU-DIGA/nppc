import json

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from rliable import library as rly
from rliable import metrics

filename = "../plottings/procgen_data.json"
with open(filename, "rb") as f:
    procgen_data_dict = json.load(f)

print(procgen_data_dict)


def convert_to_matrix(score_dict):
    keys = sorted(list(score_dict.keys()))
    return np.stack([score_dict[k] for k in keys], axis=1)


def decorate_axis(ax, wrect=10, hrect=10, labelsize="large"):
    # Hide the right and top spines
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_linewidth(2)
    ax.spines["bottom"].set_linewidth(2)
    # Deal with ticks and the blank space at the origin
    ax.tick_params(length=0.1, width=0.1, labelsize=labelsize)
    # Pablos' comment
    ax.spines["left"].set_position(("outward", hrect))
    ax.spines["bottom"].set_position(("outward", wrect))


PROCGEN_ENVS = [
    "bigfish",
    "bossfight",
    "caveflyer",
    "chaser",
    "climber",
    "coinrun",
    "dodgeball",
    "fruitbot",
    "heist",
    "jumper",
    "leaper",
    "maze",
    "miner",
    "ninja",
    "plunder",
    "starpilot",
]

EASY_GAME_RANGES = {
    "coinrun": [5, 10],
    "starpilot": [2.5, 64],
    "caveflyer": [3.5, 12],
    "dodgeball": [1.5, 19],
    "fruitbot": [-1.5, 32.4],
    "chaser": [0.5, 13],
    "miner": [1.5, 13],
    "jumper": [1, 10],
    "leaper": [1.5, 10],
    "maze": [5, 10],
    "bigfish": [1, 40],
    "heist": [3.5, 10],
    "climber": [2, 12.6],
    "plunder": [4.5, 30],
    "ninja": [3.5, 10],
    "bossfight": [0.5, 13],
}


def score_normalization_procgen(res_dict, min_scores, max_scores):
    games = res_dict.keys()
    norm_scores = {}
    for game, scores in res_dict.items():
        norm_scores[game] = (np.array(scores) - min_scores[game]) / (
                max_scores[game] - min_scores[game]
        )
    return norm_scores


MEAN_PPO_SCORES = {key: np.mean(val) for key, val in procgen_data_dict["PPO"].items()}
ZERO_SCORES = {key: 0.0 for key in PROCGEN_ENVS}
ppo_procgen_normalize = lambda scores: score_normalization_procgen(
    scores, ZERO_SCORES, MEAN_PPO_SCORES
)

MIN_PROCGEN_SCORES = {g: EASY_GAME_RANGES[g][0] for g in PROCGEN_ENVS}
MAX_PROCGEN_SCORES = {g: EASY_GAME_RANGES[g][1] for g in PROCGEN_ENVS}

min_max_procgen_normalize = lambda scores: score_normalization_procgen(
    scores, MIN_PROCGEN_SCORES, MAX_PROCGEN_SCORES
)

norm_procgen_data = {"Min-Max": {}, "PPO": {}}
algorithms = ["PPO", "MixReg", "UCB-DrAC", "PLR", "PPG", "IDAAC"]
for method in algorithms:
    scores = procgen_data_dict[method]

    norm_procgen_data["Min-Max"][method] = convert_to_matrix(
        min_max_procgen_normalize(scores)
    )
    norm_procgen_data["PPO"][method] = convert_to_matrix(ppo_procgen_normalize(scores))

pairs = [
    ["IDAAC", "PPG"],
    ["IDAAC", "UCB-DrAC"],
    ["IDAAC", "PPO"],
    ["PPG", "PPO"],
    ["UCB-DrAC", "PLR"],
    ["PLR", "MixReg"],
    ["UCB-DrAC", "MixReg"],
    ["MixReg", "PPO"],
]

procgen_algorithm_pairs = {}
for pair in pairs[::-1]:
    d1 = norm_procgen_data["Min-Max"][pair[0]]
    d2 = norm_procgen_data["Min-Max"][pair[1]]
    # d_concat = np.concatenate((d1, d2), axis=-1)
    procgen_algorithm_pairs["_".join(pair)] = (d1, d2)

probabilities, probability_cis = rly.get_interval_estimates(
    procgen_algorithm_pairs, metrics.probability_of_improvement, reps=2000
)

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(3.7, 2.1))
h = 0.6

ax2 = ax.twinx()
colors = sns.color_palette("colorblind")

for i, (pair, p) in enumerate(probabilities.items()):
    (l, u), p = probability_cis[pair], p

    ax.barh(
        y=i, width=u - l, height=h, left=l, color=colors[i], alpha=0.75, label=pair[0]
    )
    ax2.barh(
        y=i, width=u - l, height=h, left=l, color=colors[i], alpha=0.0, label=pair[1]
    )
    ax.vlines(x=p, ymin=i - 7.5 * h / 16, ymax=i + (6 * h / 16), color="k", alpha=0.85)

ax.set_yticks(list(range(len(pairs))))
ax2.set_yticks(range(len(pairs)))
pairs = [x.split("_") for x in probabilities.keys()]
ax2.set_yticklabels([pair[1] for pair in pairs], fontsize="large")
ax.set_yticklabels([pair[0] for pair in pairs], fontsize="large")
ax2.set_ylabel(
    "Algorithm Y", fontweight="bold", rotation="horizontal", fontsize="x-large"
)
ax.set_ylabel(
    "Algorithm X", fontweight="bold", rotation="horizontal", fontsize="x-large"
)
ax.set_xticks([0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
ax.yaxis.set_label_coords(-0.2, 1.0)
ax2.yaxis.set_label_coords(1.15, 1.13)
decorate_axis(ax, wrect=5)
decorate_axis(ax2, wrect=5)

ax.tick_params(axis="both", which="major", labelsize="x-large")
ax2.tick_params(axis="both", which="major", labelsize="x-large")
ax.set_xlabel("P(X > Y)", fontsize="xx-large")
ax.grid(axis="x", alpha=0.2)
# plt.subplots_adjust(wspace=0.05)
ax.spines["left"].set_visible(False)
ax2.spines["left"].set_visible(False)

plt.show()
