### How much do LLMs and the metrics agree?
import pandas as pd
import json


def transform_agentic_numerical_to_categorial_score(numeric_score):
    """Transforms the agentic/communal scores from numeric to categoric for comparison with the LLM results."""

    if numeric_score == 0:
        return "neutral"
    elif numeric_score >= 1.5:
        return "strongly female oriented"
    elif numeric_score > 0:
        return "moderately female oriented"
    elif numeric_score <= -1.5:
        return "strongly male oriented"
    elif numeric_score < 0:
        return "moderately male oriented"


def compare_columns_percentage(df1, col1, df2, col2):
    """
    Compares the string values in two pandas columns from different DataFrames
    and returns the percentage of matches.

    Parameters:
    df1 (pd.DataFrame): The first DataFrame containing the first column to compare.
    df2 (pd.DataFrame): The second DataFrame containing the second column to compare.
    col1 (str): The name of the column in the first DataFrame.
    col2 (str): The name of the column in the second DataFrame.

    Returns:
    float: The percentage of rows where the values in the two columns match.
    """
    if col1 not in df1.columns or col2 not in df2.columns:
        raise ValueError(
            f"Column '{col1}' in df1 and/or '{col2}' in df2 not found in the DataFrames."
        )

    # Ensure both DataFrames have the same length
    if len(df1) != len(df2):
        raise ValueError("The DataFrames do not have the same length.")

    total_rows = len(df1)
    if total_rows == 0:
        return 0.0

    matches = df1[col1].values == df2[col2].values
    match_percentage = matches.sum() / total_rows * 100

    return match_percentage


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
agentic_results_df = pd.read_csv("results/p_results_agentic_communal_metric.csv")
trait_results_df = pd.read_csv("results/p_results_trait_behavior.csv")

# Transform the numeric scores from agentic/communal to categorial ones for comparison.
agentic_results_df["categorical agentic communal score"] = agentic_results_df[
    "agentic communal score"
].apply(transform_agentic_numerical_to_categorial_score)

# extract the classification from the json the LLAMA API request returned
llama_p_results_df["string LLAMA classification result"] = llama_p_results_df[
    "LLAMA classification result"
].apply(extract_classification)


out_filename = "1p_results_agentic_communal.csv"
# agentic_results_df.to_csv(out_filename)

agreement_percentage = compare_columns_percentage(
    llama_p_results_df,
    "string LLAMA classification result",
    agentic_results_df,
    "categorical agentic communal score",
)
print(
    f"The percentage of matches is: {agreement_percentage:.2f}%"
)  # 26.67% agreement on the classification for the paraphrased program descriptions.
