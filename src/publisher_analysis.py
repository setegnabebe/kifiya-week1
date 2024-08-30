import pandas as pd

# Load your data
filepath = '../data/raw_analyst_ratings.csv'
data = pd.read_csv(filepath)

# If publisher names are email addresses, extract domains
if data['publisher'].str.contains('@').any():
    data['publisher_domain'] = data['publisher'].apply(lambda x: x.split('@')[-1] if '@' in x else 'unknown')
    domain_counts = data['publisher_domain'].value_counts()
    print("\nArticle Count by Publisher Domain:")
    print(domain_counts)

# Summary of Publisher Analysis
publisher_summary = data['publisher'].value_counts()
print("\nPublisher Analysis Summary:")
print(publisher_summary)