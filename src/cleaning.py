import pandas as pd 
import numpy as np 
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

def clean_training_dataframe(raw_fp):
    df = pd.read_json(raw_fp)
    df['fraud'] = df['acct_type'].str.contains('fraud')
    df_cleaned = df[['description', 'has_logo', 'listed', 'name', 'num_payouts', 'org_desc', 'user_age', 'user_type', 'fraud']]
    df_cleaned['org_description'] = (df_cleaned['org_desc']!='').astype(int)
    df_cleaned.drop('org_desc', axis=1, inplace=True)
    df_cleaned['listed']=(df_cleaned['listed']=='y').astype(int)
    return df_cleaned

def make_corpus(df_cleaned):
    docs = []
    for doc in df_cleaned['description']:
        soup = BeautifulSoup(doc, 'lxml')
        d = soup.get_text()
        d = d.replace('\n',' ').replace('\xa0','').replace("\'"," ").replace("\r"," ")
        docs.append(d)
    df_cleaned['parsed_desc'] = docs
    corpus = df_cleaned['parsed_desc']+df_cleaned['name']
    return corpus

def load_corpus():
    corpus = ['eggs are tasty, i love to eat', 'watch me pull a rabbit out of my hat', 'is it time to eat dinner yet', 'lions and tigers and bears, oh my']
    return corpus

if __name__ == "__main__":
    df = clean_training_dataframe('data/subset.json')
    corpus = make_corpus(df)
    stop_words = set(stopwords.words('english'))
    extra = ['s']
    all_stop = stop_words.union(extra)
    # vectorizer = TfidfVectorizer(stop_words=all_stop, strip_accents='ascii', ngram_range=(1,2))
    # X = vectorizer.fit_transform(corpus)
    # print(vectorizer.get_feature_names())
