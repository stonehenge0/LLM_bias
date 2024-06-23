# This script uses the concreteness  ratings provided by:
# Brysbaert, M., Warriner, A.B. & Kuperman, V. Concreteness ratings for 40 thousand generally known English word lemmas.
# Behav Res 46, 904–911 (2014). https://doi.org/10.3758/s13428-013-0403-5

import pandas as pd
import os
import spacy

nlp = spacy.load("en_core_web_sm")


def text_to_clean_wordlist(uncleaned_text):
    """Remove whitespace, punctuation and non alpha characters."""

    doc = nlp(uncleaned_text)
    clean_wordlist = [token.text for token in doc if token.is_alpha]
    return clean_wordlist


def get_brysbaert_concreteness_ratings(df, wordlist):
    """
    Sum the concreteness scores for a list of words from a given DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame with columns 'word' and 'Conc.M'.
        words (list of str): List of words to check in the DataFrame.

    Returns:
        float: The total sum of concreteness scores for the found words.
    """
    # Filter the DataFrame to include only rows where a word from the input wordlists is in the "word" column.
    filtered_df = df[df["Word"].isin(wordlist)]

    # How many words were matched in total
    number_words_matched = len(filtered_df)

    # If no words at all were matched, return
    if number_words_matched == 0:
        return ValueError  # EMMA, ob ein Value Error hier das Richtige ist?

    # Sum the concreteness ('Conc.M') values of these filtered rows
    total_score = filtered_df["Conc.M"].sum()

    # Final score is sum of all concreteness ratings / number of words matched.
    final_brysbaert_score = total_score / number_words_matched

    return final_brysbaert_score


def main():

    # Read in program descriptions and the brysbaert dataset.
    program_descriptions_df = pd.read_csv(
        "code/trait_versus_behaviour/program_descriptions.csv"
    )

    brysbaert_df = pd.read_csv(
        "code/trait_versus_behaviour/brysbaert_concreteness_ratings.csv",
    )

    # Generate clean wordlists from the program descriptions ang calculate final score for each description.
    program_descriptions_df["cleaned wordlists"] = program_descriptions_df[
        "program description"
    ].apply(text_to_clean_wordlist)
    program_descriptions_df["brysbaert score"] = program_descriptions_df[
        "cleaned wordlists"
    ].apply(lambda x: get_brysbaert_concreteness_ratings(brysbaert_df, x))

    filename_out = "results_trait_behavior.csv"
    program_descriptions_df.to_csv(filename_out)
    print(f"File has been written to:\t", filename_out)


if __name__ == "__main__":
    main()
