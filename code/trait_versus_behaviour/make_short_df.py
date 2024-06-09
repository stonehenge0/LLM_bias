import pandas as pd

# Read the dataframe from a CSV file
df = pd.read_csv('data/gendercoded_wordlists_uncleaned_results.csv')

# Make a copy of the first 3 rows
small_df_for_testing = df.head(3).copy()

# Save the smaller dataframe to a CSV file
small_df_for_testing.to_csv('small_df_for_testing.csv', index=False)

print("small_df_for_testing.csv has been created with the first 3 rows of the original dataframe.")
