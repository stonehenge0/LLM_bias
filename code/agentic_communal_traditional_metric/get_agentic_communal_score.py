# Inspiration for this script is the genderdecoder package: https://github.com/Doteveryone/genderdecoder
# The package itself is inspired by Kat Matfield's gender decoder: https://github.com/lovedaybrooke/gender-decoder

"""This script takes in the program descriptions and gives back 
a dictionary with two lists of the male and female  coded words in the original program descriptions."""

import os

import spacy
import pandas as pd
import wordlists  # see LLM_bias/code/agentic_communal_traditional_metric/wordlists.py


nlp = spacy.load("en_core_web_sm")


def preprocess(input_text):
    """Lowercase everything, remove non alphanumeric characters."""
    doc = nlp(input_text)
    cleaned_tokens = [token.text.lower() for token in doc if token.is_alpha]

    return cleaned_tokens


def get_wordlist_matches(in_text):
    """Find all matches of gender-coded words and return male and female coded wordlists."""

    # Go through all the words in the input text and return a word if it starts with any of the
    # gender coded stems from the wordlists script.
    masculine_coded_words = [
        word
        for word in in_text
        for coded_word in wordlists.masculine_coded_words
        if word.startswith(coded_word)
    ]

    feminine_coded_words = [
        word
        for word in in_text
        for coded_word in wordlists.feminine_coded_words
        if word.startswith(coded_word)
    ]

    return {
        "masculine_coded_words": masculine_coded_words,
        "feminine_coded_words": feminine_coded_words,
    }


def calculate_metric_score(
    dictionary_both_genders_wordlists, num_words_in_program_description
):
    """
    Calculate the result of the agentic/communal metric by weighting the amount of female and male
    words.
    The first argument of the input dict has to be the male list, the second one has to be the female wordlist.
    """

    # Extract gendered wordlists from the returns of the get_wordlist_matches function.
    masculine_wordlist = list(dictionary_both_genders_wordlists.values())[0]
    feminine_wordlist = list(dictionary_both_genders_wordlists.values())[1]

    count_feminine = len(feminine_wordlist)
    count_masculine = len(masculine_wordlist)

    total_count_gendered_words = count_feminine + count_masculine

    # Avoid errors because of division by zero if neither female nor male words are found.
    if total_count_gendered_words != 0:

        final_metric_score = (
            (count_feminine - count_masculine) / num_words_in_program_description
        ) * 100  # multiply by 100 just to make the final scores more readable.

    else:
        final_metric_score = 0

    return final_metric_score


def main():

    # Read in file.

    file_path = "data/rearranged_paraphrased_program_descriptions.csv"
    df = pd.read_csv(file_path)

    # Clean the program descriptions, get gendercoded wordmatches, normalize and calculate final score.
    df["gendercoded words"] = df["paraphrased program description"].apply(preprocess)
    df["wordcount program description"] = df["gendercoded words"].apply(len)
    df["gendercoded words"] = df["gendercoded words"].apply(get_wordlist_matches)
    df["agentic communal score"] = df.apply(
        lambda row: calculate_metric_score(
            row["gendercoded words"], row["wordcount program description"]
        ),
        axis=1,
    )

    # output and save the file.
    output_file = "p_results_agentic_communal_metric.csv"
    df.to_csv(output_file, index=False)
    print("Output has been written to:\t", output_file)


if __name__ == "__main__":
    main()
