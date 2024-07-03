import seaborn as sns
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


# Load the datasets
paraphrased_program_descriptions_df = pd.read_csv(
    "/home/emmastein/Documents/GitHub/LLM_bias/results/p_results_LLAMA_classification.csv"
)

original_program_descriptions_df = pd.read_csv(
    "/home/emmastein/Documents/GitHub/LLM_bias/results/results_API_LLAMA_classification.csv"
)

# Add a column and change naming a bit so we can merge the two dfs better later on.
original_program_descriptions_df["paraphrased as"] = "unmodified description"

paraphrased_program_descriptions_df.rename(
    columns={"LLAMA classification result": "LLAMA classification"}, inplace=True
)

print(paraphrased_program_descriptions_df.columns)
print(original_program_descriptions_df.columns)

# Select the columns to be concatenated (shared columns)
shared_columns = ["paraphrased as", "LLAMA classification"]

# Concatenate the shared columns
combined_df = pd.concat(
    [
        paraphrased_program_descriptions_df[shared_columns],
        original_program_descriptions_df[shared_columns],
    ],
    axis=0,
)

combined_df["LLAMA classification"] = combined_df["LLAMA classification"].apply(
    extract_classification
)

# Reset the index to ensure it is consistent
combined_df.reset_index(drop=True, inplace=True)

# order the axis
x_order = [
    "unmodified description",
    "paraphrased male",
    "paraphrased neutral",
    "paraphrased female",
]

y_order = [
    "strongly female oriented",
    "moderately female oriented",
    "neutral",
    "moderately male oriented",
    "strongly male oriented",
]

palette = {
    "unmodified description": "lightgray",
    "paraphrased male": "lightblue",
    "paraphrased neutral": "thistle",
    "paraphrased female": "pink",
}

# Convert the 'LLAMA classification' column to a categorical type with  specified order
combined_df["LLAMA classification"] = pd.Categorical(
    combined_df["LLAMA classification"], categories=y_order, ordered=True
)

# Create the violinplot
plt.figure(figsize=(10, 8))
sns.violinplot(
    x=combined_df["paraphrased as"],
    y=combined_df["LLAMA classification"],
    order=x_order,
    palette=palette,
    bw=0.4,
)

# Adjust spacing for the labels
plt.tight_layout()
plt.subplots_adjust(
    left=0.21, top=0.9
)  # Increase the left margin so the full descriptions fits.

# show plot
plt.title("Agentic/communal scores for each class of program description")
plt.xlabel("Type of paraphrase")
plt.ylabel("Agentic/communal value")
plt.show()
