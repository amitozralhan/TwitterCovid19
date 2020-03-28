from dataCollection import readRawTweets
from flask import Flask
import pandas as pd
import numpy as np
import os

from MachineLearning import TrainClassifier, Predict
from sklearn import metrics


app = Flask(__name__)
trainingDataFilePath = "TrainingData.tsv"


@app.route('/')
def hello_world():
    return 'Hello, World!'


class TweetAnalyzer():
    def tweetToDataFrame(self, tweets):
        df = pd.DataFrame(
            data=[[tweet['full_text'], tweet['id'], len(tweet['full_text']), tweet['created_at'], tweet['user']['location'], tweet['coordinates']] for tweet in tweets], columns=['Tweet', 'id', 'len', 'date', 'userLocation', 'coordinates'])

        return df

    def readTrainingData(self, filepath):
        data = pd.read_csv(filepath, sep="\t")
        return data


if __name__ == "__main__":
    # app.run()
    analyzer = TweetAnalyzer()

    trainingData = analyzer.readTrainingData(trainingDataFilePath)
    trainingDataDF = df = pd.DataFrame(
        trainingData, columns=["Classification", "Tweet", "Id"])

    trainingDataDF["Classification"].loc[trainingDataDF["Classification"]
                                         == "Infection"] = 1
    trainingDataDF["Classification"].loc[trainingDataDF["Classification"]
                                         == "Awareness"] = 0

    trainingDataDF.drop(["Id"], axis=1, inplace=True)
    trainingDataDF.dropna(inplace=True)

    # print(trainingDataDF.groupby('Classification').count())

    labels = trainingDataDF["Classification"].astype('int')

    ClassificationModel = TrainClassifier(
        trainingDataDF["Tweet"], labels)

   # predictedClasses = Predict(ClassificationModel, trainingDataDF["Tweet"])
   # print(metrics.confusion_matrix(labels, predictedClasses))

    rawData = readRawTweets()
    testDataDF = analyzer.tweetToDataFrame(rawData)
    # print(testDataDF.head())
    #predictedClasses = Predict(ClassificationModel, trainingDataDF["Tweet"])
    predictedClasses = Predict(ClassificationModel, testDataDF["Tweet"])
   # print(metrics.confusion_matrix(labels, predictedClasses))
    print(np.count_nonzero(predictedClasses == 1))
