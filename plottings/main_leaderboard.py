import gradio as gr
import pandas as pd
import numpy as np


# Generate sample performance data
def generate_performance_data():
    models = [
        "BERT-base",
        "RoBERTa-large",
        "GPT-2",
        "T5-small",
        "DeBERTa-v3",
        "XLNet",
        "ALBERT",
        "ELECTRA",
        "LLaMA-7B",
        "Mistral-7B",
        "Gemma-7B",
    ]

    # Random seed for reproducibility
    np.random.seed(42)

    data = {
        "Model Name": models,
        "Accuracy": np.random.uniform(0.82, 0.98, len(models)),
        "F1 Score": np.random.uniform(0.79, 0.97, len(models)),
        "BLEU": np.random.uniform(28.5, 45.2, len(models)),
        "ROUGE-L": np.random.uniform(0.41, 0.68, len(models)),
        "Latency (ms)": np.random.randint(45, 350, len(models)),
        "Parameters (M)": [110, 355, 1500, 60, 440, 340, 12, 110, 7000, 7000, 7000],
        "Last Updated": [
            "2024-12-15",
            "2025-01-10",
            "2024-11-21",
            "2025-01-05",
            "2024-12-30",
            "2024-11-15",
            "2024-12-10",
            "2025-01-20",
            "2024-10-25",
            "2024-11-05",
            "2025-01-30",
        ],
    }

    df = pd.DataFrame(data)
    return df


# Initial data - generate this once at the start
initial_data = generate_performance_data()
metric_choices = list(initial_data.columns)[1:]  # All columns except "Model Name"


# Leaderboard display function
def update_leaderboard(metric, ascending):
    # We'll use the already-generated data
    data = initial_data.copy()

    # Sort data based on selected metric
    sorted_data = data.sort_values(by=metric, ascending=ascending)

    # Format percentage columns
    for col in ["Accuracy", "F1 Score", "ROUGE-L"]:
        sorted_data[col] = sorted_data[col].apply(lambda x: f"{x:.2%}")

    # Format BLEU score
    sorted_data["BLEU"] = sorted_data["BLEU"].apply(lambda x: f"{x:.2f}")

    # Return sorted dataframe
    return (
        sorted_data,
        f"Leaderboard sorted by {metric} ({'ascending' if ascending else 'descending'})",
    )


# Create Gradio interface
with gr.Blocks(
    title="Nondeterministic Polynomial Problem Challenge", theme=gr.themes.Soft()
) as demo:
    gr.Markdown("# 🏆 Nondeterministic Polynomial Problem Challenge")
    gr.Markdown(
        "This leaderboard displays performance metrics for various models on NLP tasks."
    )

    with gr.Row():
        metric_dropdown = gr.Dropdown(
            choices=metric_choices,  # Use pre-defined choices
            value="Accuracy",
            label="Sort by",
        )
        ascending_checkbox = gr.Checkbox(label="Ascending order", value=False)

    update_button = gr.Button("Update Leaderboard")
    sort_info = gr.Markdown("")

    # Get initial sorted data to display
    initial_sorted_data, initial_message = update_leaderboard("Accuracy", False)

    # Use Gradio's DataFrame component with initial data
    leaderboard_table = gr.DataFrame(
        value=initial_sorted_data, interactive=False, wrap=True
    )

    gr.Markdown("---")
    gr.Markdown("Last updated: February 27, 2025 | Dataset: Multi-task NLP Benchmark")

    # Set up events
    update_button.click(
        update_leaderboard,
        inputs=[metric_dropdown, ascending_checkbox],
        outputs=[leaderboard_table, sort_info],
    )

    # Set initial info message
    demo.load(lambda: initial_message, inputs=None, outputs=sort_info)

# Launch the app
if __name__ == "__main__":
    demo.launch()
