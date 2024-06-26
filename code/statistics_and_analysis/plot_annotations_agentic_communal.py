import pandas as pd
import matplotlib.pyplot as plt
import json


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
llama_p_results_df = pd.read_csv("results/p_results_LLAMA_classification.csv")
agentic_results_df = pd.read_csv("results/1p_results_agentic_communal.csv")
# trait_results_df = pd.read_csv("results/p_results_agentic_communal.csv")

# Extract the string annotation form the original json API output.
llama_p_results_df["string LLAMA classification result"] = llama_p_results_df[
    "LLAMA classification result"
].apply(extract_classification)

# Count how often each category was annotated for the metric versus LLAMA.
llama_classification_count = llama_p_results_df[
    "string LLAMA classification result"
].value_counts()
metric_classification_count = agentic_results_df[
    "categorical agentic communal score"
].value_counts()

#################
llama_classification_count = json_data1 = {
    "moderately female oriented": 0,
    "moderately male oriented": 4,
    "neutral": 11,
    "strongy female oriented": 0,
    "strongly male oriented": 0,
}

metric_classification_count = {
    "moderately female oriented": 3,
    "moderately male oriented": 5,
    "neutral": 4,
    "strongy female oriented": 0,
    "strongly male oriented": 3,
}

# Convert JSON data to DataFrame
df1 = pd.DataFrame(
    list(llama_classification_count.items()), columns=["Category", "LLAMA_Count"]
)
df2 = pd.DataFrame(
    list(metric_classification_count.items()), columns=["Category", "Metric_Count"]
)

# Merge the DataFrames on the 'Category' column
merged_df = pd.merge(df1, df2, on="Category", how="outer").fillna(0)

# Define color sets
color_sets = [
    ["#008080", "#FF7F50"],  # Teal and Coral
    ["#000080", "#FFD700"],  # Navy and Gold
    ["#228B22", "#90EE90"],  # Forest Green and Light Green
    ["#8B0000", "#FFDAB9"],  # Dark Red and Peach
    ["#191970", "#87CEEB"],  # Midnight Blue and Sky Blue
    ["#2F4F4F", "#778899"],  # Dark Slate Gray and Light Slate Gray
    ["#DDA0DD", "#EEE8AA"],  # Plum and Pale Goldenrod
    ["#DC143C", "#DB7093"],  # Crimson and Pale Violet Red
    ["#4169E1", "#B0C4DE"],  # Royal Blue and Light Steel Blue
    ["#808000", "#F0E68C"],  # Olive and Khaki
]

# Example usage: plot with the first color set
colors = color_sets[0]  # Choose the first set (Teal and Coral)

# Plot the data
ax = merged_df.plot(
    kind="bar",
    x="Category",
    y=["LLAMA_Count", "Metric_Count"],
    figsize=(10, 6),
    width=0.8,
    color=colors,
)

# Set the labels and title with increased font size
ax.set_xlabel("Category", fontsize=14)
ax.set_ylabel("Number of Annotations", fontsize=14)
ax.set_title("Comparison of Category Annotations by LLAMA and Metric", fontsize=16)

# Customize the legend with increased font size
plt.legend(
    title="Annotations", labels=["LLAMA", "Metric"], fontsize=14, title_fontsize=16
)

# Increase the font size of category labels on the x-axis
ax.tick_params(axis="x", labelsize=14)

# Add annotations with increased font size
for p in ax.patches:
    ax.annotate(
        f"{int(p.get_height())}",
        (p.get_x() + p.get_width() / 2.0, p.get_height()),
        ha="center",
        va="center",
        xytext=(0, 10),
        textcoords="offset points",
        fontsize=14,
    )

# Show the plot
plt.tight_layout()
plt.show()
##################
