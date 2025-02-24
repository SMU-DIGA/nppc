import matplotlib.pyplot as plt

# Data
x = [5, 10, 15, 20, 25, 30, 35, 40]
y_1 = {"res": [0.42, 0.18, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0], "name": "prompt_oeqa"}
y_2 = {"res": [0.68, 0.44, 0.3, 0.06, 0.06, 0.02, 0.02, 0.0], "name": "prompt_deepseek"}

# Create figure
plt.figure(figsize=(8, 5))

# Plot the data
plt.plot(x, y_1["res"], marker='o', linestyle='-', label=y_1["name"])
plt.plot(x, y_2["res"], marker='s', linestyle='-', label=y_2["name"])

# Labels and title
plt.xlabel("X values")
plt.ylabel("Results")
plt.title("Comparison of prompt_oeqa and prompt_deepseek")
plt.legend()
plt.grid(True)

# Show the plot
plt.savefig("res_deepseek.png", dpi=300)
