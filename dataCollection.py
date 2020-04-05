import mysql.connector
from mysql.connector import Error
from tweepy import Cursor
import twitterConnectors
import config
from pymongo import MongoClient
import time


class DBConnector():
    def getCursor(self):
        try:
            self.connection = mysql.connector.connect(host=self.host,
                                                      database=self.db,
                                                      user=self.user,
                                                      password=self.pwd)
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = self.connection.cursor()
                return cursor
        except Error as e:
            print("Error while connecting to MySQL", e)

    def insertData(self, data):
        try:
            print('Data insert to database started')
            queryCursor = self.getCursor()
            mySql_insert_query = """insert ignore into TwitterData(id,CreationDate,location,text)
                            VALUES (%s, %s, %s, %s) """

            queryCursor.executemany(mySql_insert_query, data)
            self.connection.commit()
            print(queryCursor.rowcount,
                  "Records inserted successfully into Twitter table")
        except mysql.connector.Error as error:
            print("Failed to insert record into MySQL table {}".format(error))
        finally:
            if (self.connection.is_connected()):
                queryCursor.close()
                self.connection.close()
                print("MySQL connection is closed")

    def mongoConnect(self, col):
        try:
            self.conn = MongoClient('localhost', 27017)
            db = self.conn.TwitterAnalysis
            collection = db[col]
            print("Connected successfully!!!")
            return collection

        except:
            print("Could not connect to MongoDB")

    def mongoInsert(self, data, collection):

        coll = self.mongoConnect(collection)
        print(coll)
        # coll.updateMany(data, data, {'upsert': true})
        try:

            coll.insert_many(data, ordered=False)

        except:

            pass
        finally:
            self.conn.close()

    def mongoRead(self, collection):

        coll = self.mongoConnect(collection)

        d = coll.find({},
                      {'created_at': 1, 'id': 1, 'full_text': 1, 'coordinates': 1, 'user.location': 1})  # .limit(100000)

        self.conn.close()
        return d
# 'created_at':{'$regex': ".*Sat Mar 21.*"}

    def __init__(self, host, db, user, pwd):
        self.host = host
        self.db = db
        self.user = user
        self.pwd = pwd


def collectData():

    print('started collecting tweets')

    twitterClient = twitterConnectors.TwitterClient()
    api = twitterClient.getTwitterClientApi()
    tweets = Cursor(api.search, q='(covid19 OR corona OR coronavirus OR #covid19 OR #coronavirus) AND (sick OR cough OR fever OR symptoms) -filter:retweets',
                    lang="en", tweet_mode='extended', wait_on_rate_limit=True, wait_on_rate_limit_notify=True, count=1000).items(50000)

    twitter_data_json = [tweet._json for tweet in tweets]
    # print(twitter_data_json)
    print('tweet collection complete')

    twitterDB = DBConnector(config.DB_HOST, config.DATABASE,
                            config.DB_USER, config.DB_PASSWORD)

    twitterDB.mongoInsert(twitter_data_json, "RawTweets")


def readRawTweets():
    twitterDB = DBConnector(config.DB_HOST, config.DATABASE,
                            config.DB_USER, config.DB_PASSWORD)

    print('starting data read....')

    rawData = twitterDB.mongoRead("RawTweets")

    return rawData


if __name__ == "__main__":
    collectData()
