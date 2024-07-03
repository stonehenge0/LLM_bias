import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import json


def transform_orientation_to_numerical(df, column_name):
    """Map the LLAMA classification values to numerical values."""
    mapping = {
        "strongly male oriented": -2,
        "moderately male oriented": -1,
        "neutral": 0,
        "moderately female oriented": 1,
        "strongly female oriented": 2,
    }

    # Apply the mapping to the specified column
    df[column_name] = df[column_name].map(mapping)

    return df


def subtract_lists_and_plot_barplot(
    values_paraphrased, values_original, ax, title, xlim
):
    # Check if the lists are of equal length
    if len(values_paraphrased) != len(values_original):
        raise ValueError("Both lists must be of the same length.")

    # Get differences between paraphrased and original values.
    result = [val1 - val2 for val1, val2 in zip(values_paraphrased, values_original)]

    # Calculate median and average
    median_value = np.median(result)
    mean_value = np.mean(result)

    # Create a DataFrame for the result
    result_df = pd.DataFrame(result, columns=["Difference"])
    result_df["Count"] = result_df.groupby("Difference")["Difference"].transform(
        "count"
    )
    result_df = result_df.drop_duplicates().sort_values(by="Difference")

    # Plot the resulting values as a barplot
    sns.barplot(x="Difference", y="Count", data=result_df, ax=ax)

    ax.set_title(title, fontsize=16)
    ax.set_xlabel("Difference in LLM Judgement", fontsize=14)
    ax.set_ylabel("Frequency", fontsize=14)
    ax.legend(fontsize=12)

    ax.set_xlim(xlim)

    return result


def extract_classification(json_string):
    """
    Extracts the value of the 'classification' key from a JSON string.

    Parameters:
    json_string (str): The JSON string containing the data.

    Returns:
    str: The value of the 'classification' key.
    """
    try:
        data = json.loads(json_string)
        classification = data.get("classification", None)
        return classification
    except json.JSONDecodeError:
        return None


# Read in data
original_pds_df = pd.read_csv("results/results_API_LLAMA_classification.csv")
paraphrased_pds_df = pd.read_csv("results/p_results_LLAMA_classification.csv")

# Extract LLAMA classification from JSON string for both dfs
original_pds_df["LLAMA string classification"] = original_pds_df[
    "LLAMA classification"
].apply(extract_classification)
paraphrased_pds_df["LLAMA string classification"] = paraphrased_pds_df[
    "LLAMA classification result"
].apply(extract_classification)

# Make the categorical values from the LLAMA classification numerical.
df_ogriginal_transformed = transform_orientation_to_numerical(
    original_pds_df, "LLAMA string classification"
)
df_paraphrased_transformed = transform_orientation_to_numerical(
    paraphrased_pds_df, "LLAMA string classification"
)


# Split the paraphrased texts df into three dfs, depending on what they were paraphrased as.
df_female = df_paraphrased_transformed[
    df_paraphrased_transformed["paraphrased as"] == "paraphrased female"
]
df_male = df_paraphrased_transformed[
    df_paraphrased_transformed["paraphrased as"] == "paraphrased male"
]
df_neutral = df_paraphrased_transformed[
    df_paraphrased_transformed["paraphrased as"] == "paraphrased neutral"
]

# Plot the changes in LLM judgement for the three paraphrases compared to the initial judgement on the unmodified program descriptions.

# Extract the LLM scores from original and each paraphrased program description.
scores_original = df_ogriginal_transformed["LLAMA string classification"]
p_female_score = df_female["LLAMA string classification"]
p_male_score = df_male["LLAMA string classification"]
p_neutral_score = df_neutral["LLAMA string classification"]

xlim = (-1, 4)

# Create subplots
fig, axs = plt.subplots(3, 1, figsize=(12, 20), sharey=True)

# Plot each histogram
subtract_lists_and_plot_barplot(
    p_male_score, scores_original, axs[0], "Paraphrased Male", xlim
)
subtract_lists_and_plot_barplot(
    p_female_score, scores_original, axs[1], "Paraphrased Female", xlim
)

subtract_lists_and_plot_barplot(
    p_neutral_score, scores_original, axs[2], "Paraphrased Neutral", xlim
)


# Adjust layout
plt.tight_layout()
plt.subplots_adjust(hspace=0.4)
plt.show()
