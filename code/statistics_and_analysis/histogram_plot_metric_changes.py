import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def subtract_lists_and_plot_histogram(values_paraphrased, values_original):
    # Check if the lists are of equal length
    if len(values_paraphrased) != len(values_original):
        raise ValueError("Both lists must be of the same length.")

    # Subtract elements of list1 from list2
    result = [val1 - val2 for val1, val2 in zip(values_paraphrased, values_original)]

    # Calculate median and average
    median_value = np.median(result)
    mean_value = np.mean(result)

    # Plot the resulting values as a histogram using seaborn
    plt.figure(figsize=(10, 6))
    sns.histplot(result, bins=10, kde=False, color="skyblue")
    plt.axvline(
        median_value,
        color="red",
        linestyle="dashed",
        linewidth=1.5,
        label=f"Median: {median_value:.2f}",
    )
    plt.axvline(
        mean_value,
        color="green",
        linestyle="dashed",
        linewidth=1.5,
        label=f"Mean: {mean_value:.2f}",
    )
    plt.title(
        "Changes of Agentic/Communal Values in Paraphrased Female Program Descriptions"
    )
    plt.xlabel("Difference in agentic/communal Value")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True)
    plt.show()

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

# Do some testing.
l1 = [2, -2, 0, 0, 0]  # paraphrased
l2 = [-1, -1, 0, 1, -1]  # original

print(subtract_lists_and_plot_histogram(p_female_score, scores_original))
