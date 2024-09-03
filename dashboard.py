mport streamlit as st
import pandas as pd
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from scipy.stats import pearsonr
import nltk

# Download NLTK data (only need to do this once)
nltk.download('vader_lexicon')

# Streamlit app
st.title("News Sentiment and Stock Movement Correlation")

# Load datasets from static paths
news_file_path = 'data/raw_news_data.csv'  # Replace with the path to your news data CSV file
stock_file_path = 'data/raw_stock_data.csv'  # Replace with the path to your stock data CSV file

# Load datasets
news_df = pd.read_csv(news_file_path)  # Columns: 'date', 'headline'
stock_df = pd.read_csv(stock_file_path)  # Columns: 'date', 'close'

# Convert 'date' columns to datetime
news_df['date'] = pd.to_datetime(news_df['date'])
stock_df['date'] = pd.to_datetime(stock_df['date'])

# Normalize dates by grouping and aggregating
news_df = news_df.groupby(news_df['date'].dt.date).agg({'headline': ' '.join}).reset_index()
stock_df = stock_df.groupby(stock_df['date'].dt.date).agg({'close': 'last'}).reset_index()

# Merge datasets
merged_df = pd.merge(news_df, stock_df, left_on='date', right_on='date')

# Sentiment Analysis with TextBlob
def get_textblob_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

# Sentiment Analysis with NLTK
def get_nltk_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    return sid.polarity_scores(text)['compound']

# Apply sentiment analysis
merged_df['textblob_sentiment'] = merged_df['headline'].apply(get_textblob_sentiment)
merged_df['nltk_sentiment'] = merged_df['headline'].apply(get_nltk_sentiment)

# Compute daily returns
merged_df['daily_return'] = merged_df['close'].pct_change() * 100

# Aggregate Sentiments and Returns
daily_sentiments_textblob = merged_df.groupby('date')['textblob_sentiment'].mean().reset_index()
daily_sentiments_nltk = merged_df.groupby('date')['nltk_sentiment'].mean().reset_index()
daily_returns = merged_df.groupby('date')['daily_return'].mean().reset_index()

# Merge aggregated sentiments and returns
analysis_df_textblob = pd.merge(daily_sentiments_textblob, daily_returns, on='date')
analysis_df_nltk = pd.merge(daily_sentiments_nltk, daily_returns, on='date')

# Calculate Correlation
correlation_textblob, _ = pearsonr(analysis_df_textblob['textblob_sentiment'], analysis_df_textblob['daily_return'])
correlation_nltk, _ = pearsonr(analysis_df_nltk['nltk_sentiment'], analysis_df_nltk['daily_return'])

st.subheader("Analysis Results")
st.write(f"Pearson Correlation Coefficient (TextBlob): {correlation_textblob:.2f}")
st.write(f"Pearson Correlation Coefficient (NLTK): {correlation_nltk:.2f}")

# Display data
st.subheader("Merged Data")
st.write(merged_df)

st.subheader("Aggregated Data (TextBlob)")
st.write(analysis_df_textblob)

st.subheader("Aggregated Data (NLTK)")
st.write(analysis_df_nltk)
