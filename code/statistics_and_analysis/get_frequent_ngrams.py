"""Extract frequent unigrams and bigrams. """

import os

import spacy
import pandas as pd
from nltk import ngrams
from collections import Counter

nlp = spacy.load("en_core_web_sm")


def get_lemmas(text):
    """Get lemmas from a string. Removes stopwords and non alpha chars.
    Args:
        text (string)
    Output:
        lemma_list (list): list of lemmas.
    """
    doc = nlp(text)
    lemma_list = [
        token.lemma_ for token in doc if not token.is_stop and token.is_alpha
    ]  # Remove stop words and non alpha-numerical chars.
    lemma_string = " ".join(lemma_list).lower()

    return lemma_string


def get_bigrams(text, n=2):
    """Get bi-grams.
    ---
    text (string):
    n (int): scope of the n-grams. Per default this is bigrams, but can be overriden for trigrams etc.

    output"""

    ngram_counts = Counter(ngrams(text.split(), n))
    return ngram_counts


def get_unigrams(text):
    """Get unigrams with counts how often they occur."""

    unigram_counts = Counter(text.split())
    return unigram_counts


def main():
    filename = "paraphrased_program_descriptions.csv"
    parent_dir_file = "data"

    csv_file_path = os.path.join(parent_dir_file, filename)
    df = pd.read_csv(csv_file_path)

    columns_to_check = ["paraphrased neutral"]
    all_program_descriptions = df.to_string(columns=columns_to_check)
    lemma_text = get_lemmas(all_program_descriptions)

    # Final Counters of uni and bigrams.
    unigrams = str(
        get_unigrams(lemma_text).most_common(40)
    )  # Take only the most 49 frequent unigrams and 30 frequent bigrams
    bigrams = str(get_bigrams(lemma_text).most_common(30))

    output_file = "common_ngrams_p_neutral.txt"

    with open(output_file, "a") as file:
        # Write the string to the file
        file.write(unigrams)
        file.write(bigrams)

    print()
    print("Output saved to: ", output_file)
    print()


if __name__ == "__main__":
    main()
