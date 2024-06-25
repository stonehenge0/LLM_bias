import json
import csv
import pandas as pd

path_to_paraphrased_pds = "data/paraphrased_program_descriptions.csv"
df = pd.read_csv(path_to_paraphrased_pds)
# Delete the original program description, so we can melt the df later.
df = df.drop("program description", axis=1)


def convert_to_json(json_str):
    """Convert JSON string to JSON object"""
    try:
        return json.loads(json_str)
    except (TypeError, json.JSONDecodeError):
        return json_str


def extract_values(data):
    """
    Recursively extracts all values from a nested dictionary and concatenates them into one string.
    """
    values = []

    def extract(data):
        if isinstance(data, dict):
            for value in data.values():
                extract(value)
        elif isinstance(data, list):
            for item in data:
                extract(item)
        else:
            values.append(str(data))

    extract(data)
    return " ".join(values)


# Transform input from string to json.
# This is kinda redundant, maybe chang eht syntax of functin later.
df["paraphrased female"] = df["paraphrased female"].apply(convert_to_json)
df["paraphrased male"] = df["paraphrased male"].apply(convert_to_json)
df["paraphrased neutral"] = df["paraphrased neutral"].apply(convert_to_json)


# Melt the DataFrame to have a df that has all the descriptions under each other and keeps the program id etc.
melted_df = pd.melt(
    df,
    id_vars=["program-id", "program name"],
    value_vars=["paraphrased female", "paraphrased male", "paraphrased neutral"],
    var_name="paraphrased as",
    value_name="paraphrased program description",
)
# Make the json objects to strings for readability.
melted_df["paraphrased program description"] = melted_df[
    "paraphrased program description"
].apply(extract_values)


melted_df.to_csv(
    "rearranged_paraphrased_program_descriptions.csv",
    index=False,
    quoting=csv.QUOTE_MINIMAL,
)
