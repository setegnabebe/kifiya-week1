import streamlit as st
import pandas as pd
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import analysis  # Import the analysis module from the src directory

# Load the dataset
@st.cache_data
def load_data():
    # Replace with the actual path to your CSV file
    data = pd.read_csv('../data/raw_analyst_ratings.csv')
    return data

df = load_data()

# Print the column names to verify
st.write("Columns in the dataset:")
st.write(df.columns)

# Descriptive Statistics
st.header('Descriptive Statistics')

# Textual Lengths
st.subheader('Textual Lengths')
if 'headline' in df.columns:
    length_stats = analysis.calculate_textual_lengths(df)
    st.write(length_stats)
else:
    st.error("Column 'headline' is missing from the dataset.")

# Article Count by Publisher
st.subheader('Article Count by Publisher')
if 'publisher' in df.columns:
    publisher_counts = analysis.count_articles_by_publisher(df)
    st.bar_chart(publisher_counts)
else:
    st.error("Column 'publisher' is missing from the dataset.")

# Publication Dates
st.subheader('Publication Dates')
if 'date' in df.columns:
    date_counts = analysis.analyze_publication_dates(df)
    st.line_chart(date_counts)
else:
    st.error("Column 'date' is missing from the dataset.")

# Text Analysis
st.header('Text Analysis')

# Sentiment Analysis
st.subheader('Sentiment Analysis')
if 'headline' in df.columns:
    df = analysis.perform_sentiment_analysis(df)
    sentiment_counts = df['sentiment_label'].value_counts()
    st.bar_chart(sentiment_counts)
else:
    st.error("Column 'headline' is missing from the dataset.")

# Topic Modeling
st.subheader('Top 20 Keywords')
if 'headline' in df.columns:
    top_terms = analysis.extract_topics(df)
    st.bar_chart(top_terms.head(20).set_index('term')['count'])
else:
    st.error("Column 'headline' is missing from the dataset.")

# Time Series Analysis
st.header('Time Series Analysis')

# Publication Frequency
st.subheader('Publication Frequency')
if 'date' in df.columns:
    publication_freq = analysis.analyze_publication_frequency(df)
    st.line_chart(publication_freq)
else:
    st.error("Column 'date' is missing from the dataset.")

# Publishing Times
st.subheader('Publishing Times')
if 'date' in df.columns:
    time_counts = analysis.analyze_publishing_times(df)
    st.line_chart(time_counts)
else:
    st.error("Column 'date' is missing from the dataset.")

# Publisher Analysis
st.header('Publisher Analysis')

# Publisher Contribution
st.subheader('Publisher Contribution')
if 'publisher' in df.columns:
    publisher_contribution = analysis.analyze_publisher_contribution(df)
    st.bar_chart(publisher_contribution)
else:
    st.error("Column 'publisher' is missing from the dataset.")

# Publisher Email Domains
st.subheader('Publisher Email Domains')
if 'publisher' in df.columns:
    domain_counts = analysis.analyze_email_domains(df)
    st.bar_chart(domain_counts)
else:
    st.error("Column 'publisher' is missing from the dataset.")