import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-GUI environments

import pandas as pd
import matplotlib.pyplot as plt

# Load your data
filepath = '../data/raw_analyst_ratings.csv'
try:
    data = pd.read_csv(filepath)
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit()

# Print columns to debug
print("Columns in the dataset:")
print(data.columns)

# Ensure 'date' and 'headline' columns are present
required_columns = ['date', 'headline', 'publisher']
missing_columns = [col for col in required_columns if col not in data.columns]

if missing_columns:
    print(f"Error: Missing columns in the dataset: {', '.join(missing_columns)}")
    exit()

# Convert 'date' to datetime
data['date'] = pd.to_datetime(data['date'], errors='coerce')

# Handle any conversion issues
if data['date'].isnull().any():
    print("Warning: Some publication dates could not be converted and are now NaT.")

# Drop rows with NaT in 'date'
data.dropna(subset=['date'], inplace=True)

# Calculate headline length
data['headline_length'] = data['headline'].apply(len)

# Basic statistics for headline lengths
print("\nHeadline Length Statistics:")
print(data['headline_length'].describe())

# Count of articles per publisher
publisher_counts = data['publisher'].value_counts()
print("\nNumber of Articles per Publisher:")
print(publisher_counts)

# Trends over time
daily_articles = data.groupby(data['date'].dt.date).size()

plt.figure(figsize=(12, 6))
plt.plot(daily_articles.index, daily_articles.values, marker='o', linestyle='-')
plt.title('Number of Articles Published Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Articles')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('articles_over_time.png')  # Save plot as an image file
print("Plot saved as 'articles_over_time.png'")
