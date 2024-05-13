"""Create a version of the program description data so we can vote out false positives (agentic/communal). 
-> hide names of the programs and get local contexts of target words to judge them in context."""

import os

import pandas as pd
import json 

from wordlist_matches import preprocess


def get_local_context(program_description_tokens, target_words, length_context_window=4):
    """Get the local context of a list of target words in a given text.
    
    Parameters:
        program_description_tokens (list): A cleaned list of tokens (cleaned = no punctuations/whitespace)
        target_words (list): the target word(s) to find the local context of
        length_context_window (int): Size of context window. Default = 4

    Returns: 
        full_context (list of tuples): Each entry in the list is one word and its local context. 
                                       First element of a tuple is the target word, second is its context.
    """
    # Ensure target_words is a list
    if isinstance(target_words, str):
        target_words = [target_words]
    
    full_context = []

    
    for target_word in target_words:

        positions = [i for i, word in enumerate(program_description_tokens) if word == target_word]

        for pos in positions:
            # Make sure start and end are within list bounds
            start = max(0, pos - length_context_window)
            end = min(len(program_description_tokens), pos + length_context_window + 1)

            
            context = " ".join(program_description_tokens[start:end])

            full_context.append((target_word, context))

    return full_context


def extract_values(s):
    """ Extract values from a JSON-like string representation stored in a CSV file."""

    # Replace single quotes with double quotes to make JSON-compatible,
    # cause JSON format requires double quotes for keys and values
    s = s.replace("'",'"') 

    # Parse JSON string to a Python dictionary
    d = json.loads(s) 

    return  list(d.values())

def pretty_print_tuples(tuples_list):
    """Pretty print a list of tuples into strings seperated by newlines for readability."""

    return '\n\n'.join(f"{word}: {context}" for word, context in tuples_list)


file_path = os.path.join("data", "gendercoded_wordlists_uncleaned_results.csv")
absolute_file_path = os.path.abspath(file_path)
df = pd.read_csv(absolute_file_path)




df["gendercoded wordlists"] = df["gendercoded words"].apply(extract_values)
df["cleaned pds"] = df["program description"].apply(preprocess) # make sure we have clean tokens.



df["male words"] = df["gendercoded wordlists"].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None)
df["female words"] = df["gendercoded wordlists"].apply(lambda x: x[1] if isinstance(x, list) and len(x) > 0 else None)


# get local context for each word in the gendercoded list
df['male words with context'] = df.apply(
    lambda row: get_local_context(row['cleaned pds'], row['male words']),
    axis=1
)
df['female words with context'] = df.apply(
    lambda row: get_local_context(row['cleaned pds'], row['female words']),
    axis=1
)

# make them pretty to read. 
df['Male Pretty Printed Tuples'] = df["male words with context"].apply(pretty_print_tuples)
df['Female Pretty Printed Tuples'] = df["female words with context"].apply(pretty_print_tuples)

# Get rid of columns not needed for the voting.
columns_to_drop = [
    "program name",
    "dominant gender immatriculation",
    'program description',
    'cleaned pds',
    "male words",
    "female words",
    "male words with context",
    "female words with context",
    "gendercoded words"
]
df.drop(columns_to_drop, axis=1, inplace=True)

out_file_name = "vote_out_false_positives_original_program_descriptions.csv"
df.to_csv(out_file_name, index = False) # give me the award for the longest filename already

print(f"Output has been written to:\t", out_file_name)