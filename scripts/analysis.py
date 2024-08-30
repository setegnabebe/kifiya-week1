import pandas as pd
from textblob import TextBlob
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def calculate_textual_lengths(df):
    """Calculate headline lengths and return statistics."""
    if 'headline' in df.columns:
        df['headline_length'] = df['headline'].apply(len)
        length_stats = df['headline_length'].describe()
        return length_stats
    else:
        raise KeyError("Column 'headline' is missing from the dataset.")

def count_articles_by_publisher(df):
    """Count the number of articles by publisher."""
    if 'publisher' in df.columns:
        publisher_counts = df['publisher'].value_counts()
        return publisher_counts
    else:
        raise KeyError("Column 'publisher' is missing from the dataset.")

def analyze_publication_dates(df):
    """Analyze publication dates."""
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        date_counts = df['date'].value_counts().sort_index()
        return date_counts
    else:
        raise KeyError("Column 'date' is missing from the dataset.")

def perform_sentiment_analysis(df):
    """Perform sentiment analysis on the headlines."""
    if 'headline' in df.columns:
        def get_sentiment(text):
            analysis = TextBlob(text)
            return analysis.sentiment.polarity

        df['sentiment'] = df['headline'].apply(get_sentiment)
        df['sentiment_label'] = pd.cut(df['sentiment'], bins=[-1, -0.1, 0.1, 1], labels=['Negative', 'Neutral', 'Positive'])
        return df
    else:
        raise KeyError("Column 'headline' is missing from the dataset.")

def extract_topics(df, num_topics=5, num_words=10):
    """Extract topics from headlines using LDA."""
    if 'headline' in df.columns:
        vectorizer = CountVectorizer(stop_words='english')
        dtm = vectorizer.fit_transform(df['headline'])
        lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
        lda.fit(dtm)
        
        topics = []
        for i, topic in enumerate(lda.components_):
            top_words = [vectorizer.get_feature_names_out()[index] for index in topic.argsort()[-num_words:]]
            topics.append({'term': " ".join(top_words), 'count': topic.sum()})
        return pd.DataFrame(topics)
    else:
        raise KeyError("Column 'headline' is missing from the dataset.")

def analyze_publication_frequency(df):
    """Analyze publication frequency over time."""
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        publication_freq = df.set_index('date').resample('D').size()
        return publication_freq
    else:
        raise KeyError("Column 'date' is missing from the dataset.")

def analyze_publishing_times(df):
    """Analyze publishing times."""
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['hour'] = df['date'].dt.hour
        time_counts = df['hour'].value_counts().sort_index()
        return time_counts
    else:
        raise KeyError("Column 'date' is missing from the dataset.")

def analyze_publisher_contribution(df):
    """Analyze publisher contribution as a percentage."""
    if 'publisher' in df.columns:
        publisher_contribution = df['publisher'].value_counts(normalize=True) * 100
        return publisher_contribution
    else:
        raise KeyError("Column 'publisher' is missing from the dataset.")

def analyze_email_domains(df):
    """Analyze email domains if publisher names are email addresses."""
    if 'publisher' in df.columns:
        if df['publisher'].str.contains('@').any():
            df['publisher_domain'] = df['publisher'].apply(lambda x: x.split('@')[-1] if '@' in x else 'unknown')
            domain_counts = df['publisher_domain'].value_counts()
            return domain_counts
        else:
            return df['publisher'].value_counts()
    else:
        raise KeyError("Column 'publisher' is missing from the dataset.")
