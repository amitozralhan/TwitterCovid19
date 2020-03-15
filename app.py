
from pprint import pprint
import numpy as np

import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


from dataCollection import readRawTweets
from twitterConnectors import TweetAnalyzer
from vectorization import clusterData


def dataCleaner(data):

    print('data cleaning started')

    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    cleanData = []
    for row in data:
        word_tokens = word_tokenize(row[3])
        filtered_sentence = " ".join(
            [ps.stem(w) for w in word_tokens if not w in stop_words])
        cleanData.append((row[0], row[1], row[2], row[3], filtered_sentence))
    print('data cleaning completed')
    return cleanData


if __name__ == "__main__":

    data = readRawTweets()
    tweetText = [tweet['full_text'] for tweet in data]
    #analyzer = TweetAnalyzer()

    #tweetDF = analyzer.tweetToDataFrame(data)
    # print(tweetText)
    clusterData(tweetText)
