# this is not finished, first draft :) 

import os 
import re

test = "colorless ambitious ideas sleep furiously." # Make Chomsky proud.

# right now these are just toy words.  
male_words = ["ambition", "aggression", "excellence"]
female_words = ["together", "communal", "good"] 

male_counter = 0
female_counter = 0

def count_matches(expression, text):
    # Compile the regular expression pattern
    pattern = re.compile(expression)
    
    # Use findall to get all matches
    matches = pattern.findall(text)
    
    # Return the count of matches
    return len(matches)


expression = r'anyword*' # cries in but-what-escape-character-is-not-used-in-regex       
    
print(count_matches(expression, test))  
