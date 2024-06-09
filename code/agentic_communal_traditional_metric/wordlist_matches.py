# Inspiration for this script is the genderdecoder package: https://github.com/Doteveryone/genderdecoder
# The package itself is inspired by Kat Matfield's gender decoder: https://github.com/lovedaybrooke/gender-decoder 

"""This script takes in the program descriptions and gives back 
a dictionary with two lists of the male and female  coded words in the original program descriptions."""

import os

import spacy 
import pandas as pd
import wordlists # see agentic_communal_traditional_metric/wordlists.py


nlp = spacy.load("en_core_web_sm")

def preprocess(input_text):
    """Lowercase everything, remove non alphanumeric characters."""
    doc = nlp(input_text)
    cleaned_tokens = [token.text.lower() for token in doc if token.is_alpha]

    return cleaned_tokens

def get_wordlist_matches(in_text):
    """Finds all matches of gender-coded words and returns male and female coded words."""


    # Goes through all the words in the input text and returns that word if it starts with any of the 
    # gender coded stems from the wordlists script.
    masculine_coded_words = [word for word in in_text
        for coded_word in wordlists.masculine_coded_words
        if word.startswith(coded_word)]
    
    feminine_coded_words = [word for word in in_text
        for coded_word in wordlists.feminine_coded_words
        if word.startswith(coded_word)]
    
    return {
            "masculine_coded_words": masculine_coded_words,
            "feminine_coded_words": feminine_coded_words
            }

def main():


    # Define the relative path to the file
    file_path = os.path.join("data", "program_descriptions.csv")

    # Get the absolute path to the file
    absolute_file_path = os.path.abspath(file_path)


    df = pd.read_csv(absolute_file_path)

    # Apply both functions from above to each entry in the program descriptions column.
    df['gendercoded words'] = df['program description'].apply(lambda x: preprocess(x))
    df['gendercoded words'] = df['gendercoded words'].apply(lambda x: get_wordlist_matches(x))

    output_file = "gendercoded_wordlists_uncleaned_results.csv"
    df.to_csv(output_file, index = False)
    print("Output has been written to:\t", output_file)


if __name__ == '__main__':
    main()

