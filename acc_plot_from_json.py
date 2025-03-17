import json
import os

import matplotlib.pyplot as plt


def plot_accuracy_from_json(json_file, model_name, problem_name, n_shots, save_path):
    # Extract problem name from the filename
    problem_name = f"{model_name} - {problem_name} - {n_shots} shots"

    # Load JSON data
    with open(json_file, "r") as f:
        data = json.load(f)

    # Extract levels and accuracies
    levels = [int(entry["level"]) for entry in data]
    accuracies = [float(entry["accuracy"]) for entry in data]

    # Plot
    plt.figure(figsize=(8, 6))
    plt.plot(levels, accuracies, marker="o", linestyle="-", color="b")
    plt.xlabel("Level")
    plt.ylabel("Accuracy")
    plt.title(problem_name)
    plt.xticks(levels)
    plt.ylim(0, 1)
    plt.grid(True)
    plt.savefig(save_path)


model_name = "deepseek"
n_shots = 3
problem_list = ["three_sat", "clique", "vertex_cover"]
for problem_name in problem_list:
    json_file = os.path.join(
        "./results", problem_name, model_name, f"shots_{n_shots}_summary.json"
    )
    save_path = os.path.join(
        "./results",
        problem_name,
        model_name,
        f"{problem_name}_{model_name}_{n_shots}_shots_accuracy_plot.png",
    )
    plot_accuracy_from_json(json_file, model_name, problem_name, n_shots, save_path)
