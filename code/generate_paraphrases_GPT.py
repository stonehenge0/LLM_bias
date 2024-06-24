"""This script calls GPT4 and asks it to paraphrase the program descriptions in the csv file as 
male, female or neutral oriented."""

import pandas as pd
from openai import OpenAI


client = OpenAI()  # Requires an OpenAI API key.


# The three functions are almost identical, except the passage that targets the different genders.
# But just grammatically it wasn't possible to combine them into one function and have the prompts be grammatically correct.
# So it looks a bit redundant on first glance.


def paraphrase_as_f(program_description):
    """Prompt to generate a female targeted paraphrase."""

    response = client.chat.completions.create(
        model="gpt-4o",
        seed=42,  # seed for reproducibility
        temperature=1,  # temerature for randomness, temperature can be between 0 and 2.
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant designed to output JSON.",  # output as json object.
            },
            {
                "role": "system",
                "content": "You are the coordinator and responsible for writing academic program descriptions for a university.",
            },
            {
                "role": "user",
                "content": "You need to rewrite the current program description provided below for the university website. This description was written by a previous program coordinator in order to attract female candidates to the program, but the percentage of women did not change after that. Rewrite the text to make more women want to apply to this program. Use a vocabulary that speaks and correlates to women according to your understanding. Please also incorporate the values that are important to women in the text to help improve the program description. The resulting text should be cohesive and follow an academic style of writing. Please think and organize your tasks step-by-step. The text is the following:",
            },
            {"role": "user", "content": program_description},
        ],
    )

    output = response.choices[0].message.content

    return output


def paraphrase_as_m(program_description):
    """Prompt to generate a male targeted paraphrase."""

    response = client.chat.completions.create(
        model="gpt-4o",
        seed=42,  # seed for reproducibility
        temperature=1,  # temerature for randomness, temperature can be between 0 and 2.
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant designed to output JSON.",  # output as json object.
            },
            {
                "role": "system",
                "content": "You are the coordinator and responsible for writing academic program descriptions for a university.",
            },
            {
                "role": "user",
                "content": "You need to rewrite the current program description provided below for the university website. This description was written by a previous program coordinator in order to attract male candidates to the program, but the percentage of men did not change after that. Rewrite the text to make more men want to apply to this program. Use a vocabulary that speaks and correlates to men according to your understanding. Please also incorporate the values that are important to men in the text to help improve the program description. The resulting text should be cohesive and follow an academic style of writing. Please think and organize your tasks step-by-step.The text is the following:",
            },
            {"role": "user", "content": program_description},
        ],
    )

    output = response.choices[0].message.content

    return output


def paraphrase_as_n(program_description):
    """Prompt to generate a paraphrase targeted equally at male and female audiences."""

    response = client.chat.completions.create(
        model="gpt-4o",
        seed=42,  # seed for reproducibility
        temperature=1,  # temerature for randomness, temperature can be between 0 and 2.
        response_format={"type": "json_object"},  # output as json object.
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant designed to output JSON.",  # output as json object.
            },
            {
                "role": "system",
                "content": "You are the coordinator and responsible for writing academic program descriptions for a university.",
            },
            {
                "role": "user",
                "content": "You need to rewrite the current program description provided below for the university website. This description was written by a previous program coordinator in order to attract candidates of both genders equally to the program, but the percentage of candidates did not get more even between genders. Rewrite the text to make more people of both genders want to apply to this program. Use a vocabulary that speaks and correlates to both genders according to your understanding. Please also incorporate the values that are important to both genders in the text to help improve the program description. The resulting text should be cohesive and follow an academic style of writing. Please think and organize your tasks step-by-step. The text is the following:",
            },
            {"role": "user", "content": program_description},
        ],
    )

    output = response.choices[0].message.content

    return output


csv_file_path = "program_descriptions.csv"
df = pd.read_csv(csv_file_path)


# Apply the paraphrasing functions to create new columns
df["paraphrased female"] = df["program description"].apply(paraphrase_as_f)
df["paraphrased male"] = df["program description"].apply(paraphrase_as_m)
df["paraphrased neutral"] = df["program description"].apply(paraphrase_as_n)


output_filename = "final_paraphrased_program_descriptions.csv"
df.to_csv(output_filename, index=False)

print(f"Output has been written to: {output_filename}")
