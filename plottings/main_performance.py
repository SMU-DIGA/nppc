import numpy as np
import matplotlib.pyplot as plt
from npeval import plot_utils
from npeval.interval import get_interval_estimates
from npeval import metrics

num_runs = 5
num_tasks = 100
num_frames = 200
nppc_result = {
    "gpt-4o": np.random.rand(num_runs, num_tasks, num_frames),
    "gpt-4o-mini": np.random.rand(num_runs, num_tasks, num_frames),
    "claude": np.random.rand(num_runs, num_tasks, num_frames),
    "deepseek": np.random.rand(num_runs, num_tasks, num_frames),
    "o1": np.random.rand(num_runs, num_tasks, num_frames),
}

ale_all_frames_scores_dict = nppc_result
frames = np.array([1, 10, 25, 50, 75, 100, 125, 150, 175, 200]) - 1
ale_frames_scores_dict = {
    algorithm: score[:, :, frames]
    for algorithm, score in ale_all_frames_scores_dict.items()
}
iqm = lambda scores: np.array(
    [metrics.aggregate_iqm(scores[..., frame]) for frame in range(scores.shape[-1])]
)
iqm_scores, iqm_cis = get_interval_estimates(ale_frames_scores_dict, iqm, reps=2000)

fig, ax = plt.subplots(figsize=(7, 4.5))
plot_utils.plot_sample_efficiency_curve(
    frames + 1,
    iqm_scores,
    iqm_cis,
    algorithms=list(nppc_result.keys()),
    xlabel=r"Number of Frames (in millions)",
    ylabel="IQM Human Normalized Score",
    ax=ax,
)

plt.show()
