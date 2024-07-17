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
    ax.set_title(title, fontsize=16)
    ax.set_xlabel("Difference in trait/behavior value", fontsize=14)
    ax.set_ylabel("Frequency", fontsize=14)
    ax.legend(fontsize=12)
    ax.set_xlim(xlim)

    # Increase font size for axis labels
    ax.tick_params(axis="both", which="major", labelsize=12)

    return result


# Read in data
df_og = pd.read_csv("results/results_trait_behavior.csv")
df_p = pd.read_csv("results/p_results_trait_behavior.csv")

# Split the paraphrased program descriptions according to what they were paraphrased as.
df_female = df_p[df_p["paraphrased as"] == "paraphrased female"]
df_male = df_p[df_p["paraphrased as"] == "paraphrased male"]
df_neutral = df_p[df_p["paraphrased as"] == "paraphrased neutral"]

# extract brysbaert scores from original and paraphrased program descriptions
p_female_score = df_female["brysbaert score"]
p_male_score = df_male["brysbaert score"]
p_neutral_score = df_neutral["brysbaert score"]

scores_original = df_og["brysbaert score"]

# This calculatoin of min/max seems kinda off, but we'll se what it does for now:
# Calculate global x-axis limits
all_results = [val1 - val2 for val1, val2 in zip(p_female_score, scores_original)] + [
    val1 - val2 for val1, val2 in zip(p_male_score, scores_original)
]

global_min = min(all_results)
global_max = max(all_results)
xlim = (global_min, global_max)

# Create subplots
fig, axs = plt.subplots(3, 1, figsize=(12, 12), sharey=True)

# Plot each histogram
subtract_lists_and_plot_histogram(
    p_male_score, scores_original, axs[0], "Paraphrased Male", xlim
)
subtract_lists_and_plot_histogram(
    p_female_score, scores_original, axs[1], "Paraphrased Female", xlim
)
subtract_lists_and_plot_histogram(
    p_neutral_score, scores_original, axs[2], "Paraphrased Neutral", xlim
)

# Adjust layout
plt.tight_layout()
plt.show()
