from dataCollection import readRawTweets

from vectorization import clusterData
from flask import Flask
import pandas as pd

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


class TweetAnalyzer():
    def tweetToDataFrame(self, tweets):
        df = pd.DataFrame(
            data=[[tweet['full_text'], tweet['id'], len(tweet['full_text']), tweet['created_at'], tweet['user']['location'], tweet['coordinates']] for tweet in tweets], columns=['Tweet', 'id', 'len', 'date', 'userLocation', 'coordinates'])
        # for tweet in tweets:
        #     print(tweet['id'])
        return df

# def dataCleaner(data):

#     print('data cleaning started')

#     stop_words = set(stopwords.words('english'))
#     ps = PorterStemmer()
#     cleanData = []
#     for row in data:
#         word_tokens = word_tokenize(row[3])
#         filtered_sentence = " ".join(
#             [ps.stem(w) for w in word_tokens if not w in stop_words])
#         cleanData.append((row[0], row[1], row[2], row[3], filtered_sentence))
#     print('data cleaning completed')
#     return cleanData


if __name__ == "__main__":
    # app.run()

    data = readRawTweets()

    analyzer = TweetAnalyzer()

    tweetDF = analyzer.tweetToDataFrame(data)
    tweetExport = tweetDF[['id', 'Tweet']].sample(frac=0.01)
    tweetExport.to_csv('TrainingData.csv', sep='\t',
                       index=False, encoding='utf-8')
    print(tweetExport)
    # clusterData(tweetText)
