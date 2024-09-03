import pandas as pd
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import os

# Download NLTK data (only need to do this once)
nltk.download('vader_lexicon')

# Define file path
news_filepath = 'pages/raw_analyst_ratings.csv'

# Check if the file exists
if not os.path.isfile(news_filepath):
    print(f"Error: The file '{news_filepath}' does not exist.")
    exit()

# Function for sentiment analysis using TextBlob
def get_textblob_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

# Function for sentiment analysis using NLTK
def get_nltk_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    return sid.polarity_scores(text)['compound']

# Load news data
try:
    news_df = pd.read_csv(news_filepath)
except Exception as e:
    print(f"Error loading the CSV file: {e}")
    exit()

# Display news data
print("### News Data")
print(news_df.head())

# Ensure necessary columns are present
if 'date' in news_df.columns and 'headline' in news_df.columns:
    # Convert date column to datetime, letting pandas infer the format
    news_df['date'] = pd.to_datetime(news_df['date'], errors='coerce')

    # Perform sentiment analysis
    news_df['textblob_sentiment'] = news_df['headline'].apply(get_textblob_sentiment)
    news_df['nltk_sentiment'] = news_df['headline'].apply(get_nltk_sentiment)

    # Display data with sentiment analysis
    print("### News Data with Sentiment Scores")
    print(news_df.head())

    # Save data with sentiment scores
    try:
        news_df.to_csv('news_data_with_sentiment.csv', index=False)
        print("Data saved successfully to 'news_data_with_sentiment.csv'")
    except Exception as e:
        print(f"Error saving the CSV file: {e}")
else:
    print("The CSV file must contain 'date' and 'headline' columns.")
