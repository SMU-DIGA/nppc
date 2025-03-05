import numpy as np
import matplotlib.pyplot as plt

# Set data
categories = ["Speed", "Reliability", "Comfort", "Safety", "Efficiency"]
product_A = [4.2, 3.8, 5.0, 4.7, 3.5]
product_B = [3.8, 4.5, 3.2, 4.0, 5.0]

# Number of variables
N = len(categories)

# Compute angle for each category
angles = [n / float(N) * 2 * np.pi for n in range(N)]

# We need to repeat the first value to close the circular graph
product_A = np.append(product_A, product_A[0])
product_B = np.append(product_B, product_B[0])
angles = np.append(angles, angles[0])
categories = np.append(categories, categories[0])

# Initialize the plot
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

# Draw one axis per variable and add labels
plt.xticks(angles[:-1], categories[:-1], size=12)

# Plot data
ax.plot(angles, product_A, "b-", linewidth=2, label="Product A")
ax.fill(angles, product_A, "b", alpha=0.1)
ax.plot(angles, product_B, "r-", linewidth=2, label="Product B")
ax.fill(angles, product_B, "r", alpha=0.1)

# Set y-axis limits
ax.set_ylim(0, 5.5)

# Add legend
plt.legend(loc="upper right", bbox_to_anchor=(0.1, 0.1))

# Add a title
plt.title("Product Comparison", size=15)

plt.tight_layout()
plt.savefig('radar.pdf', bbox_inches="tight")

plt.show()
