import json
import matplotlib.pyplot as plt
import os
import json
import re

def read_json_files(directory):
    data = []

    # Define the regex pattern to extract model, problem, and num_shots
    pattern = re.compile(r"model_(.+)_problem_(.+)_shots_(\d+)\.json")

    # Iterate through files in the directory
    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            model_name, problem_name, num_shots = match.groups()
            num_shots = int(num_shots)  # Convert shots to integer
            
            # Get full file path
            file_path = os.path.join(directory, filename)

            data.append({
                "model_name": model_name,
                "problem_name": problem_name,
                "num_shots": num_shots,
                "file_path": file_path,  # Include file path
            })
    
    return data


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

# Example Usage
directory_path = "./results_online"  # Change to your actual directory
json_data = read_json_files(directory_path)

# Print extracted information
for entry in json_data:
    print(f"Model: {entry['model_name']}, Problem: {entry['problem_name']}, Shots: {entry['num_shots']}")
    os.makedirs(directory_path + "_plots", exist_ok=True)
    save_path = os.path.join(directory_path + "_plots", f"{entry['model_name']}_{entry['problem_name']}_{entry['num_shots']}.png")
    plot_accuracy_from_json(entry["file_path"], entry['model_name'], entry['problem_name'], entry['num_shots'], save_path)

model_name = "deepseek-r1"
n_shots = 1
problem_list = ["three_sat", "clique", "vertex_cover"]
# ["independent_set", "partition", "set_packing", "set_splitting", "subset_sum"]
# for problem_name in problem_list:
#     json_file = os.path.join(
#         "./results", problem_name, model_name, f"shots_{n_shots}_summary.json"
#     )
#     save_path = os.path.join(
#         "./results",
#         problem_name,
#         model_name,
#         f"{problem_name}_{model_name}_{n_shots}_shots_accuracy_plot.png",
#     )
#     plot_accuracy_from_json(json_file, model_name, problem_name, n_shots, save_path)