import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class RadarChart:
    def __init__(self, categories, values, title="Radar Chart"):
        """
        Initialize the RadarChart class.

        Parameters:
        -----------
        categories : list
            List of category names for each axis
        values : list or list of lists
            Single set of values or multiple sets for comparison
        title : str
            Title of the radar chart
        """
        self.categories = categories
        self.values = values
        self.num_vars = len(categories)
        self.title = title

    def plot(self, figsize=(10, 10), colors=None, grid=True):
        """
        Create and display the radar chart.

        Parameters:
        -----------
        figsize : tuple
            Figure size in inches (width, height)
        colors : list
            List of colors for different data sets
        grid : bool
            Whether to show the grid lines
        """
        # Calculate angles for each category
        angles = [n / float(self.num_vars) * 2 * np.pi for n in range(self.num_vars)]
        angles += angles[:1]  # Complete the circle

        # Create figure and polar subplot
        fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(projection="polar"))

        # Set default colors if none provided

        colors = sns.color_palette("colorblind")

        # Plot multiple datasets if provided
        if isinstance(self.values[0], (list, np.ndarray)):
            for idx, value_set in enumerate(self.values):
                values = np.concatenate(
                    (value_set, [value_set[0]])
                )  # Complete the circle
                ax.plot(
                    angles,
                    values,
                    linewidth=2,
                    linestyle="solid",
                    color=colors[idx % len(colors)],
                    label=f"Dataset {idx + 1}",
                )
                ax.fill(angles, values, color=colors[idx % len(colors)], alpha=0.25)
        else:
            # Plot single dataset
            values = np.concatenate((self.values, [self.values[0]]))
            ax.plot(
                angles,
                values,
                linewidth=2,
                linestyle="solid",
                color=colors[0],
                label="Values",
            )
            ax.fill(angles, values, color=colors[0], alpha=0.25)

        # Set category labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(self.categories)

        # Add grid
        if grid:
            ax.grid(True)

        # Add legend and title
        plt.legend(loc="upper right", bbox_to_anchor=(0.1, 0.1))
        plt.title(self.title, size=20, y=1.05)

        return fig, ax


# Example usage
if __name__ == "__main__":
    # Define categories and data
    categories = ["Math", "English", "Physics", "Chemistry", "Biology", "History"]

    # Single dataset example
    values1 = [90, 85, 88, 83, 95, 87]

    # Multiple datasets example
    values2 = [
        [90, 85, 88, 83, 95, 87],  # Student A
        [85, 90, 92, 87, 88, 85],  # Student B
    ]

    # Create radar chart with single dataset
    radar1 = RadarChart(categories, values1, "Student Performance Radar Chart")
    fig1, ax1 = radar1.plot()
    # plt.savefig("single_radar.png")
    plt.close()

    # Create radar chart with multiple datasets
    radar2 = RadarChart(categories, values2, "Students Performance Comparison")
    fig2, ax2 = radar2.plot()

    # plt.savefig("comparison_radar.png")
    plt.show()
    # plt.close()
