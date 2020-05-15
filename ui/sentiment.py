'''
Conduct Sentiment Analysis
Chun Hu, Yimin Li, Tianyue Niu
'''

import os
import json
import re
import pandas as pd
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

# turn off warnings
pd.set_option('mode.chained_assignment', None)

cwd = os.path.dirname(__file__)
top_10s_path = os.path.join(cwd, 'top10s.csv')


def merge_two_df(top_songs, lyrics):
    '''
    Input:
        top_songs (pandas data frame): kaggle data
        lyrics (json file): lyrics scraped
    Output:
        a merged data containing lyrics (pandas data frame)
    '''

    # merge two df
    top_songs['lyrics'] = ''
    for index, row in top_songs.iterrows():
        tit = top_songs.title[index]
        if tit in lyrics:
            top_songs['lyrics'][index] = lyrics[tit]

    return top_songs


def process_words(words, stop):
    '''
    Input:
        words (list): a list of words
        stop (list): extra stop words we want to remove
    Output:
        new_words (list): a list of normalized words
    '''
    lemmatizer = WordNetLemmatizer()
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_word = new_word.lower()
            if new_word not in stop and new_word not in stopwords.words('english'):
                new_word = lemmatizer.lemmatize(new_word, pos='v')
                new_words.append(new_word)
    return new_words


def add_sentiment(top_songs):
    '''
    Input:
        top_songs (pandas df): raw version
    Output:
        top_songs (pandas df): with sentiment analysis result
    '''

    # tokenize words
    top_songs['tokenized'] = top_songs['lyrics'].apply(\
        lambda x: [word_tokenize(s) for s in sent_tokenize(x)])

    # normalize words
    top_songs['normalized'] = top_songs['tokenized']
    stop = ['chorus', 'verse', 'intro', 'pre', 'outro', 'interlude']
    for index, row in top_songs['tokenized'].items():
        new_sent = []
        for sent in row:
            new_sent += process_words(sent, stop)
        top_songs['normalized'][index] = new_sent

    # calculate sentiment
    top_songs['sentiment'] = ''
    for index, row in top_songs.iterrows():
        obj = TextBlob(' '.join(top_songs['normalized'][index]))
        sentiment = obj.sentiment.polarity
        top_songs['sentiment'][index] = sentiment

    return top_songs


def create_final_top_songs ():
    '''
    Input:
        None
    Output:
        top_songs (pandas df): final cleaned & processed data frame
    '''

    top_songs = pd.read_csv(top_10s_path)

    with open('lyrics_file.json') as f:
        lyrics = json.load(f)

    top_songs = merge_two_df(top_songs, lyrics)
    df = add_sentiment(top_songs)

    df.to_csv('top_songs.csv')

    return


if __name__ == "__main__":
    create_final_top_songs()
