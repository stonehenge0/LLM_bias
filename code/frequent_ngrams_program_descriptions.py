import os

import spacy
import pandas as pd
import csv
from nltk import ngrams
from collections import Counter

nlp = spacy.load("en_core_web_sm")
txt = "test"


def get_lemmas (text):
    """Get lemmas from a string. Removes stopwords and non alpha chars.
    Args:
        text (string)  
    Output: 
        lemma_list (list): list of lemmas (strings, not hashes).
    """
    doc = nlp(text)
    lemma_list = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    lemma_string = " ".join(lemma_list)
    
    return lemma_string

def get_bigrams (text, n = 2): 
    """Get bi-grams. 
    ---
    text (string):
    n (int): scope of the n-grams. Per default this is bigrams, but can be overriden for trigrams etc.
    
    output """
    

    ngram_counts = Counter(ngrams(text.split(), n))
    return(ngram_counts)

def get_unigrams (text): 
    """Get unigrams with counts how often they occur."""
    
    unigram_counts = Counter(text.split())    
    return unigram_counts
 
    
    
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
csv_file_path = os.path.join(parent_dir, 'data', 'program_descriptions.csv')
    
program_descriptions = pd.read_csv(csv_file_path)

print(program_descriptions.head())

    
# You'll need to lemmatize them before getting the uni and bigrams. 
#lemma_text = get_lemmas(text)


if __name__ == "__main__":
    main()