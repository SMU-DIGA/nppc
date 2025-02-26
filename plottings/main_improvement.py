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


pairs = []

algorithms = list(nppc_result.keys())
num_algorithms = len(algorithms)

for i in range(num_algorithms):
    for j in range(i + 1, num_algorithms):
        pairs.append([algorithms[i], algorithms[j]])

nppc_pairs = {}
for pair in pairs[::-1]:
    d1 = nppc_result[pair[0]]
    d2 = nppc_result[pair[1]]
    # d_concat = np.concatenate((d1, d2), axis=-1)
    nppc_pairs["_".join(pair)] = (d1, d2)

probabilities, probability_cis = get_interval_estimates(
    nppc_pairs, metrics.probability_of_improvement, reps=2000
)

plot_utils.plot_probability_of_improvement(
    probability_estimates=probabilities,
    probability_interval_estimates=probability_cis,
    pair_separator="_",
)

plt.show()
