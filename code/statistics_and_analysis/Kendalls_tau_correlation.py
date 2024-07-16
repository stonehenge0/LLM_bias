"""Calculate Kendall's tau, a correlation coefficient for ordinal data. It analyses whether the LLM judgement and 
traditional metrics are correlated."""

import pandas as pd
from scipy.stats import kendalltau

# Example data
data = {
    "Item": ["A", "B", "C", "D", "E"],
    "Category": ["Low", "Medium", "High", "Medium", "High"],
    "Numerical Score": [5, 15, 25, 10, 20],
}

# Create DataFrame
df = pd.DataFrame(data)

# Convert categories to ranks
category_to_rank = {"Low": 1, "Medium": 2, "High": 3}
df["Category Rank"] = df["Category"].map(category_to_rank)

# Print DataFrame
print("Data with ranks:")
print(df)

# Calculate Kendall's tau
tau, p_value = kendalltau(df["Category Rank"], df["Numerical Score"])

print(f"\nKendall's tau: {tau}")
print(f"P-value: {p_value}")
