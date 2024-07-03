import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def subtract_lists_and_plot_histogram(
    values_paraphrased, values_original, ax, title, xlim
):
    # Check if the lists are of equal length
    if len(values_paraphrased) != len(values_original):
        raise ValueError("Both lists must be of the same length.")

    # Subtract elements of list1 from list2
    result = [val1 - val2 for val1, val2 in zip(values_paraphrased, values_original)]

    # Get median and average
    median_value = np.median(result)
    mean_value = np.mean(result)

    # Plot the resulting values as a histogram using seaborn
    sns.histplot(result, bins=15, kde=False, ax=ax)
    ax.axvline(
        median_value,
        color="red",
        linestyle="dashed",
        linewidth=1.5,
        label=f"Median: {median_value:.2f}",
    )
    ax.axvline(
        mean_value,
        color="green",
        linestyle="dashed",
        linewidth=1.5,
        label=f"Mean: {mean_value:.2f}",
    )
    ax.set_title(title)
    ax.set_xlabel("Difference in agentic/communal Value")
    ax.set_ylabel("Frequency")
    ax.legend()
    ax.set_xlim(xlim)

    return result


# Read in data
original_pds_df = pd.read_csv("results/results_agentic_communal_metric.csv")
paraphrased_pds_df = pd.read_csv("results/1p_results_agentic_communal.csv")

# Extract the agentic/communal scores from original and paraphrased program descriptions.
scores_original = original_pds_df["agentic communal score"]

# Split the paraphrased program descriptions according to what they were paraphrased as.
df_female = paraphrased_pds_df[
    paraphrased_pds_df["paraphrased as"] == "paraphrased female"
]
df_male = paraphrased_pds_df[paraphrased_pds_df["paraphrased as"] == "paraphrased male"]
df_neutral = paraphrased_pds_df[
    paraphrased_pds_df["paraphrased as"] == "paraphrased neutral"
]

# Extract the agentic/communal scores from the paraphrased program descriptions.
p_female_score = df_female["agentic communal score"]
p_male_score = df_male["agentic communal score"]
p_neutral_score = df_neutral["agentic communal score"]

# Calculate global x-axis limits
all_results = [val1 - val2 for val1, val2 in zip(p_female_score, scores_original)] + [
    val1 - val2 for val1, val2 in zip(p_male_score, scores_original)
]

global_min = min(all_results)
global_max = max(all_results)
xlim = (global_min, global_max)

# Create subplots
fig, axs = plt.subplots(3, 1, figsize=(12, 12))

# Plot each histogram
subtract_lists_and_plot_histogram(
    p_male_score, scores_original, axs[0], "Paraphrased Male", xlim
)
subtract_lists_and_plot_histogram(
    p_female_score, scores_original, axs[1], "Paraphrased Female", xlim
)
subtract_lists_and_plot_histogram(
    p_neutral_score, scores_original, axs[2], "Paraphrased Female", xlim
)


# Adjust layout
plt.tight_layout()
plt.show()
