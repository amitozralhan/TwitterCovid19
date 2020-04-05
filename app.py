from dataCollection import readRawTweets
from flask import Flask
import pandas as pd
import numpy as np
import os
from matplotlib import pyplot
from scipy import interpolate

from MachineLearning import TrainClassifier, Predict


app = Flask(__name__)
trainingDataFilePath = "TrainingData.tsv"
resultsFilePath = "PredictedResults.tsv"


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


def predictUnseenData(ClassificationModel):
    analyzer = TweetAnalyzer()
    rawData = readRawTweets()
    testDataDF = analyzer.tweetToDataFrame(rawData)
    # print(testDataDF.head())
    predictedClasses = Predict(ClassificationModel, testDataDF["Tweet"])
    print(
        f'Positive Prediction count from unseen data: {np.count_nonzero(predictedClasses == 1)}')
    testDataDF["Classification"] = predictedClasses

    testDataDF['date'] = pd.to_datetime(testDataDF['date']).dt.date
    return testDataDF


def visualizePredictedData():
    predictedUnseenData = pd.read_csv(
        resultsFilePath, sep="\t", lineterminator='\n', low_memory=False)
    plotData = predictedUnseenData.groupby(
        ['date', 'Classification']).count()['Tweet'].unstack()
    plotData['percentagePositive'] = plotData[1]*100/(plotData[1]+plotData[0])
    plotData['percentageNegative'] = plotData[0]*100/(plotData[1]+plotData[0])

    plotData = plotData.reset_index()

    plotData.plot(kind='line', x='date', y=[
                  'percentagePositive'])
    pyplot.show()


if __name__ == "__main__":
    # app.run()
    analyzer = TweetAnalyzer()

    # read Training Data and remove NAs. Also convert classification labels to 1s and 0s

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

    ################ train model using training data ##############################

    ClassificationModel = TrainClassifier(
        trainingDataDF["Tweet"], labels, "NB")

    ClassificationModel = TrainClassifier(
        trainingDataDF["Tweet"], labels, "SVM")
    ClassificationModel = TrainClassifier(
        trainingDataDF["Tweet"], labels, "KNN")

    #######################Predict the unseen raw data from Mongo DB approx 1.5 million tweets ################################
    predictedUnseenData = predictUnseenData(ClassificationModel)

    predictedUnseenData.to_csv(resultsFilePath, sep="\t")
    visualizePredictedData()
