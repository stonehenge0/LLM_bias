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

    # Go through all the words in the input text and returns that word if it starts with any of the
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


def calculate_metric_score(dictionary_both_genders_wordlists):
    """
    Calculate the result of the agentic/communal metric by weighting the amount of female and male
    words.
    The first argument has to be the male list, the second one has to be the female wordlist.
    """

    # Extract gendered wordlists from the returns of the get_wordlist_matches function.
    masculine_wordlist = list(dictionary_both_genders_wordlists.keys())[0]
    feminine_wordlist = list(dictionary_both_genders_wordlists.keys())[1]

    count_feminine = len(feminine_wordlist)
    count_masculine = len(masculine_wordlist)

    total_count_gendered_words = count_feminine + count_masculine

    # Avoid errors because of division by zero if neither female nor male words are found.
    if total_count_gendered_words != 0:

        final_metric_score = (
            count_feminine - count_masculine
        ) / total_count_gendered_words

    else:
        final_metric_score = 0

    return final_metric_score


def main():

    # Get filepath.
    file_path = os.path.join("data", "program_descriptions.csv")
    absolute_file_path = os.path.abspath(file_path)

    df = pd.read_csv(absolute_file_path)

    # Clean the program descriptions, extract gendered words and calculate the final metric score.
    df["gendercoded words"] = df["program description"].apply(lambda x: preprocess(x))
    df["gendercoded words"] = df["gendercoded words"].apply(
        lambda x: get_wordlist_matches(x)
    )
    df["agentic communal score"] = df[
        "gendercoded words"
    ].apply  # Hier dann den Namen von dem Ding oben einfügen

    output_file = "gendercoded_wordlists_results.csv"
    df.to_csv(output_file, index=False)
    print("Output has been written to:\t", output_file)


if __name__ == "__main__":
    main()

# Check that the functin and everything actually works
# If it does, replace this output with the one currently in the "data" repo.
