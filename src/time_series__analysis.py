import matplotlib
matplotlib.use('Agg')  # Use 'Agg' backend for non-interactive plotting

import pandas as pd
import matplotlib.pyplot as plt

# Load your data
filepath2 = '../data/raw_analyst_ratings.csv'
try:
    data = pd.read_csv(filepath2)
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit()

# Print columns to debug
print("Columns in the dataset:")
print(data.columns)

# Ensure 'date' column is present
if 'date' not in data.columns:
    print("Error: 'date' column is missing in the dataset.")