import config
from tweepy.streaming import StreamListener
from tweepy import API

from tweepy import OAuthHandler
from tweepy import Stream
import pandas as pd
import twitterConnectors


class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate()
        self.twitter_user = twitter_user

    def getTwitterClientApi(self):
        self.twitter_client = API(
            self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        return self.twitter_client


class TwitterAuthenticator():

    def authenticate(self):
        auth = OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET_KEY)
        auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
        return auth


class TwitterStreamer():
    """
    Class for streaming twitter data
    """

    def __init__(self):
        self.twitterAuth = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweet_filename, has_tag_list):
        listener = TwitterListener(fetched_tweet_filename)
        auth = self.twitterAuth.authenticate()

        stream = Stream(auth, listener)
        stream.filter(track=has_tag_list)


class TwitterListener(StreamListener):
    """
    base class that prints received tweets
    """

    def __init__(self, fetched_tweet_filename):
        self.fetched_tweet_filename = fetched_tweet_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweet_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print(f"error on data ${e}")

    def on_error(self, status):
        if status == 420:
            return False
        print(status)
