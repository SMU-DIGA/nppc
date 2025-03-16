import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

colors = sns.color_palette("colorblind")
algs = ["SLAC", "SAC+AE", "Dreamer", "PISAC", "RAD", "DrQ"]

color_idxs = [0, 3, 4, 2, 1] + list(range(9, 4, -1))
DMC_COLOR_DICT = dict(zip(algs, [colors[idx] for idx in color_idxs]))

mean_ranks_all = {
    "100k": np.array(
        [
            [0.10743, 0.20364167, 0.23485417, 0.18149917, 0.22783917, 0.04473583],
            [0.00525583, 0.02049667, 0.026895, 0.07802583, 0.24528917, 0.6240375],
            [0.10036, 0.13595167, 0.22296333, 0.26617917, 0.153905, 0.12064083],
            [0.48958417, 0.23752083, 0.143075, 0.07609917, 0.0409425, 0.01277833],
            [0.06477833, 0.12616, 0.16300583, 0.24148083, 0.22734917, 0.17722583],
            [0.23259167, 0.27622917, 0.20920667, 0.15671583, 0.104675, 0.02058167],
        ]
    ),
    "500k": np.array(
        [
            [0.09359417, 0.2333175, 0.27359833, 0.19462, 0.11536333, 0.08950667],
            [0.00051917, 0.0101825, 0.0508725, 0.13493417, 0.2900825, 0.51340917],
            [0.23326333, 0.184615, 0.15467083, 0.13140583, 0.190735, 0.10531],
            [0.452315, 0.26775833, 0.14475167, 0.08371833, 0.0375525, 0.01390417],
            [0.04386083, 0.08181833, 0.13780667, 0.22876, 0.26725917, 0.240495],
            [0.1764475, 0.22230833, 0.2383, 0.22656167, 0.0990075, 0.037375],
        ]
    ),
}

keys = algs
labels = list(range(1, len(keys) + 1))
width = 1.0  # the width of the bars: can also be len(x) sequence

# fig, axes = plt.subplots(ncols=2, figsize=(2.9 * 2, 3.6))
fig, axes = plt.subplots(nrows=2, figsize=(2, 2.3 * 2))

for main_idx, main_key in enumerate(["100k", "500k"]):
    ax = axes[main_idx]
    mean_ranks = mean_ranks_all[main_key]
    bottom = np.zeros_like(mean_ranks[0])
    for i, key in enumerate(algs):
        label = key if main_idx == 0 else None
        ax.bar(
            labels,
            mean_ranks[i],
            width,
            label=label,
            color=DMC_COLOR_DICT[key],
            bottom=bottom,
            alpha=0.9,
        )
        bottom += mean_ranks[i]

    yticks = np.array(range(0, 101, 20))
    ax.set_yticklabels(yticks, size="large")
    if main_idx == 0:
        ax.set_ylabel("Fraction (in %)", size="x-large")
        yticks = np.array(range(0, 101, 20))
        ax.set_yticklabels(yticks, size="large")
    else:
        ax.set_yticklabels([])

    ax.set_yticks(yticks * 0.01)
    # ax.set_xlabel('Ranking', size='x-large')
    if main_idx != 0:
        ax.set_xticks(labels)
    else:
        ax.set_xticks([])
    # ax.set_xticklabels(labels, size='large')
    ax.set_title(main_key + " steps", size="x-large", y=0.95)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    # left = True if main_idx == 0 else False
    left = True
    ax.tick_params(
        axis="both",
        which="both",
        bottom=False,
        top=False,
        left=left,
        right=False,
        labeltop=False,
        labelbottom=True,
        labelleft=left,
        labelright=False,
    )

fig.legend(
    loc="center right",
    fancybox=True,
    ncol=1,
    fontsize="x-large",
    bbox_to_anchor=(2.05, 0.40),
)
fig.subplots_adjust(top=0.72, wspace=0.0, bottom=0)
fig.text(x=-0.2, y=0.2, s="Fraction (in %)", rotation=90, size="xx-large")
plt.show()

# keys = algs
# labels = list(range(1, len(keys)+1))
# width = 1.0       # the width of the bars: can also be len(x) sequence
#
# fig, axes = plt.subplots(nrows=1, ncols=6, figsize=(14, 3.5))
# all_ranks = all_ranks_individual['500k']
# for task in range(6):
#   bottom = np.zeros_like(mean_ranks[0])
#   for i, key in enumerate(keys):
#     ranks = all_ranks[task]
#     ax = axes[task]
#     ax.bar(labels, ranks[i], width, color=DMC_COLOR_DICT[key],
#            bottom=bottom, alpha=0.9)
#     bottom += ranks[i]
#     # for label in labels:
#       # perc = int(np.round(mean_ranks[i][label-1] * 100))
#       # ax.text(s= str(perc) + '%', x=label-0.25, y=bottom[label-1] - perc/200,
#       #         color="w", verticalalignment="center",
#       #         horizontalalignment="left", size=10)
#     ax.set_title(DMC_ENVS[task], fontsize='large')
#
#   # if task == 0:
#   #   ax.set_ylabel('Fraction (in %)', size='x-large')
#   #   yticks = np.array(range(0, 101, 20))
#   #   ax.set_yticklabels(yticks, size='large')
#   # else:
#   #   ax.set_yticklabels([])
#
#   if task == 0:
#     ax.set_ylabel('Distribution', size='x-large')
#   ax.set_xlabel('Ranking', size='x-large')
#   ax.set_xticks(labels)
#   ax.set_ylim(0, 1)
#   ax.set_xticklabels(labels, size='large')
#   ax.spines['top'].set_visible(False)
#   ax.spines['right'].set_visible(False)
#   ax.spines['bottom'].set_visible(False)
#   ax.spines['left'].set_visible(False)
#   ax.tick_params(axis='both', which='both', bottom=False, top=False,
#                   left=False, right=False, labeltop=False,
#                   labelbottom=True, labelleft=False, labelright=False)
#
# fake_patches = [mpatches.Patch(color=DMC_COLOR_DICT[m], alpha=0.75)
#                 for m in keys]
# legend = fig.legend(fake_patches, keys, loc='upper center',
#                     fancybox=True, ncol=len(keys), fontsize='x-large')
# fig.subplots_adjust(top=0.78, wspace=0.1, hspace=0.05)
# plt.show()
