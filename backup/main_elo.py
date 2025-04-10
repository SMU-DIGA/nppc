from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class EloCalculator:
    """
    ELO Rating Calculator for comparing algorithm performance across multiple tasks.

    This class implements the ELO rating system to evaluate and compare the relative
    performance of different algorithms on various tasks. The ELO system works by
    updating ratings based on the outcome of pairwise comparisons between algorithms.
    """

    def __init__(self, initial_rating=1500, k_factor=32):
        """
        Initialize the ELO Calculator.

        Parameters:
        - initial_rating: Starting rating for all algorithms (default: 1500)
        - k_factor: Factor controlling the magnitude of rating adjustments (default: 32)
        """
        self.initial_rating = initial_rating
        self.k_factor = k_factor

    def expected_score(self, rating_a, rating_b):
        """
        Calculate the expected score (probability of winning) for algorithm A against B.

        Parameters:
        - rating_a: Current rating of algorithm A
        - rating_b: Current rating of algorithm B

        Returns:
        - Expected score for algorithm A (between 0 and 1)
        """
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

    def update_rating(self, rating, expected, actual):
        """
        Update an algorithm's rating based on the match outcome.

        Parameters:
        - rating: Current rating
        - expected: Expected score
        - actual: Actual score (1 for win, 0.5 for draw, 0 for loss)

        Returns:
        - Updated rating
        """
        return rating + self.k_factor * (actual - expected)

    def calculate_elo_from_performance(self, performance_matrix):
        """
        Calculate ELO ratings based on a performance matrix.

        Parameters:
        - performance_matrix: DataFrame where rows are algorithms, columns are tasks,
                             and values are performance metrics (higher is better)

        Returns:
        - Dictionary mapping algorithm names to their final ELO ratings
        """
        algorithms = performance_matrix.index
        num_algorithms = len(algorithms)

        # Initialize ratings
        ratings = {alg: self.initial_rating for alg in algorithms}

        # Process all tasks
        for task in performance_matrix.columns:
            # Get performance values for current task
            task_performance = performance_matrix[task]

            # Compare all possible algorithm pairs
            for alg_a, alg_b in combinations(algorithms, 2):
                # Get performance scores
                score_a = task_performance[alg_a]
                score_b = task_performance[alg_b]

                # Determine match outcome based on performance scores
                if score_a > score_b:
                    actual_a = 1
                    actual_b = 0
                elif score_a < score_b:
                    actual_a = 0
                    actual_b = 1
                else:
                    actual_a = 0.5
                    actual_b = 0.5

                # Calculate expected scores
                expected_a = self.expected_score(ratings[alg_a], ratings[alg_b])
                expected_b = self.expected_score(ratings[alg_b], ratings[alg_a])

                # Update ratings
                ratings[alg_a] = self.update_rating(
                    ratings[alg_a], expected_a, actual_a
                )
                ratings[alg_b] = self.update_rating(
                    ratings[alg_b], expected_b, actual_b
                )

        return ratings

    def visualize_ratings(self, ratings, title="Algorithm ELO Ratings Comparison"):
        """
        Create a bar chart visualizing algorithm ELO ratings.

        Parameters:
        - ratings: Dictionary mapping algorithm names to ELO ratings
        - title: Chart title

        Returns:
        - Matplotlib plot object
        """
        algorithms = list(ratings.keys())
        scores = list(ratings.values())

        plt.figure(figsize=(10, 6))
        bars = plt.bar(algorithms, scores, color="skyblue")

        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 5,
                f"{height:.1f}",
                ha="center",
                va="bottom",
            )

        plt.xlabel("Algorithms")
        plt.ylabel("ELO Rating")
        plt.title(title)
        plt.ylim(min(scores) - 100, max(scores) + 100)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()

        return plt


# Example usage
def main():
    """
    Example demonstrating how to use the ELO calculator with custom data.
    """
    # Create sample data for 5 algorithms on 10 tasks
    algorithms = [
        "Algorithm A",
        "Algorithm B",
        "Algorithm C",
        "Algorithm D",
        "Algorithm E",
    ]
    tasks = [f"Task {i + 1}" for i in range(10)]

    # Example 1: Using "higher is better" metrics (like accuracy, F1-score, etc.)
    print("==== Example 1: Using metrics where higher values are better ====")

    # Generate random performance data (replace with real data in actual use)
    # Values between 0-100, where higher values indicate better performance
    np.random.seed(42)  # For reproducibility
    performance_data = np.random.rand(5, 10) * 100
    performance_df = pd.DataFrame(performance_data, index=algorithms, columns=tasks)

    print("Performance matrix (higher values = better performance):")
    print(performance_df.round(2))
    print("\n")

    # Calculate ELO ratings
    elo_calculator = EloCalculator(initial_rating=1500, k_factor=32)
    ratings = elo_calculator.calculate_elo_from_performance(performance_df)

    print("Final ELO Ratings (ranked):")
    for alg, rating in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
        print(f"{alg}: {rating:.2f}")

    # Visualize ratings
    plt = elo_calculator.visualize_ratings(ratings)
    # plt.savefig('algorithm_elo_ratings.png', dpi=300, bbox_inches='tight')  # Uncomment to save the figure
    plt.show()

    # Example 2: Using "lower is better" metrics (like error rates, latency, etc.)
    print("\n==== Example 2: Using metrics where lower values are better ====")

    # Generate random error rate data (0-20%)
    np.random.seed(123)
    error_rates = np.random.rand(5, 10) * 0.2
    error_df = pd.DataFrame(error_rates, index=algorithms, columns=tasks)

    print("Error rates (lower values = better performance):")
    print(error_df.round(4))
    print("\n")

    # For "lower is better" metrics, we need to invert the values
    # Option 1: Take the negative value
    inverted_performance = -error_df

    # Calculate ELO ratings using the inverted performance
    ratings2 = elo_calculator.calculate_elo_from_performance(inverted_performance)

    print("Final ELO Ratings based on error rates (ranked):")
    for alg, rating in sorted(ratings2.items(), key=lambda x: x[1], reverse=True):
        print(f"{alg}: {rating:.2f}")

    # Visualize ratings
    plt = elo_calculator.visualize_ratings(
        ratings2, title="Algorithm ELO Ratings (based on error rates)"
    )
    plt.show()

    # Example 3: Custom NLP algorithm comparison
    print("\n==== Example 3: NLP Algorithms Comparison ====")

    nlp_algorithms = ["GPT-4", "BERT", "RoBERTa", "XLNet", "T5"]
    nlp_tasks = [
        "Text Classification",
        "Sentiment Analysis",
        "Question Answering",
        "Summarization",
        "Machine Translation",
        "Named Entity Recognition",
        "Text Generation",
        "Semantic Similarity",
        "Relation Extraction",
        "Textual Entailment",
    ]

    # Sample performance data (accuracy scores)
    data = {
        "GPT-4": [0.92, 0.90, 0.88, 0.89, 0.87, 0.91, 0.94, 0.88, 0.86, 0.89],
        "BERT": [0.86, 0.85, 0.80, 0.79, 0.81, 0.87, 0.83, 0.84, 0.82, 0.85],
        "RoBERTa": [0.88, 0.87, 0.82, 0.81, 0.83, 0.89, 0.85, 0.86, 0.83, 0.87],
        "XLNet": [0.87, 0.86, 0.83, 0.82, 0.82, 0.88, 0.84, 0.85, 0.84, 0.86],
        "T5": [0.90, 0.88, 0.85, 0.87, 0.86, 0.90, 0.89, 0.87, 0.85, 0.88],
    }

    # Convert to DataFrame and transpose (algorithms as rows, tasks as columns)
    nlp_df = pd.DataFrame(data, index=nlp_tasks).T

    print("NLP algorithm performance (accuracy):")
    print(nlp_df)
    print("\n")

    # Calculate ELO ratings
    nlp_ratings = elo_calculator.calculate_elo_from_performance(nlp_df)

    print("Final ELO Ratings for NLP algorithms (ranked):")
    for alg, rating in sorted(nlp_ratings.items(), key=lambda x: x[1], reverse=True):
        print(f"{alg}: {rating:.2f}")

    # Visualize NLP ratings
    plt = elo_calculator.visualize_ratings(
        nlp_ratings, title="NLP Algorithm ELO Ratings"
    )
    plt.show()


if __name__ == "__main__":
    main()
