import os

import spacy
import pandas as pd
from nltk import ngrams
from collections import Counter

nlp = spacy.load("en_core_web_sm")


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
csv_file_path = os.path.join('data', 'program_descriptions.csv')
    
df = pd.read_csv(csv_file_path)

full_text = ""

columns_to_check = ["program description"]
full_text= df.to_string(columns= columns_to_check)

print(full_text[:10])
    
     
    

    
# You'll need to lemmatize them before getting the uni and bigrams. 
#lemma_text = get_lemmas(text)