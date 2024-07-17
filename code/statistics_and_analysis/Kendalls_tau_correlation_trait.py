"""Calculate Kendall's tau, a correlation coefficient for ordinal data. It analyses whether the LLM judgement and 
the agentic metric are correlated."""

import pandas as pd
from scipy.stats import kendalltau
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


#################################################
# Now we do the same for LLAMA.
###################################################
llama_original_df = pd.read_csv("results/results_API_LLAMA_classification.csv")
llama_paraphrased_df = pd.read_csv("results/p_results_LLAMA_classification.csv")

## Make original LLAMA dataframe into the right format.
columns_to_keep = ["program-id", "program name", "LLAMA classification"]
llama_original_df = llama_original_df[columns_to_keep]
llama_original_df["LLAMA classification"] = llama_original_df[
    "LLAMA classification"
].apply(extract_classification)

llama_original_df.insert(2, "paraphrased as", "original program description")

print(llama_original_df.columns)


## Make paraphrased LLAMA into the right format.
columns_to_keep = [
    "program-id",
    "program name",
    "paraphrased as",
    "LLAMA classification result",
]
llama_paraphrased_df = llama_paraphrased_df[columns_to_keep]
llama_paraphrased_df["LLAMA classification"] = llama_paraphrased_df[
    "LLAMA classification result"
].apply(extract_classification)

llama_paraphrased_df.drop(columns=["LLAMA classification result"], inplace=True)

# Combine the two dataframes
llama_df = pd.concat([llama_original_df, llama_paraphrased_df])


####################################################################
# And now we can calculate Kendall's tau for the two dataframes.
##################################################################

# Convert categorial data to ranks from the LLAMA classification.
category_to_rank = {
    "strongly male oriented": 1,
    "moderately male oriented": 2,
    "neutral": 3,
    "moderately female oriented": 4,
    "strongly female oriented": 5,
}
llama_df["LLAMA classification"] = llama_df["LLAMA classification"].map(
    category_to_rank
)

# Print DataFrame
print("Data with ranks:")
print(llama_df)

# Calculate Kendall's tau
tau, p_value = kendalltau(
    llama_df["LLAMA classification"], agentic_df["agentic communal score"]
)

print(f"\nKendall's tau: {tau}")
print(f"P-value: {p_value}")
