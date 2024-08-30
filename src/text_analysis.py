import pandas as pd
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Load your data
filepath='../data/raw_analyst_ratings.csv'
data = pd.read_csv(filepath)

# Sentiment Analysis
def get_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

data['sentiment'] = data['headline'].apply(get_sentiment)
data['sentiment_label'] = pd.cut(data['sentiment'], bins=[-1, -0.1, 0.1, 1], labels=['Negative', 'Neutral', 'Positive'])

print("\nSentiment Analysis:")
print(data['sentiment_label'].value_counts())

# Topic Modeling
def get_topics(texts, num_topics=5, num_words=10):
    vectorizer = CountVectorizer(stop_words='english')
    dtm = vectorizer.fit_transform(texts)
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda.fit(dtm)
    
    topics = []
    for i, topic in enumerate(lda.components_):
        top_words = [vectorizer.get_feature_names_out()[index] for index in topic.argsort()[-num_words:]]
        topics.append(f"Topic {i}: " + " ".join(top_words))
    return topics

topics = get_topics(data['headline'])
print("\nTopics Extracted:")
for topic in topics:
    print(topic)
