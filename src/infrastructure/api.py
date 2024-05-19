import os
from amazon.paapi import AmazonAPI
from requests_oauthlib import OAuth1


POST_TWEET_ENDPOINT = "https://api.twitter.com/2/tweets"
MEDIA_UPLOAD_ENDPOINT = "https://upload.twitter.com/1.1/media/upload.json"


def auth_amazon_api():
    ACCESS_KEY = os.getenv("ACCESS_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ASSOCIATE_ID = os.getenv("ASSOCIATE_ID")
    COUNTRY = "JP"

    return AmazonAPI(ACCESS_KEY, SECRET_KEY, ASSOCIATE_ID, COUNTRY)


def auth_twitter_api():
    CONSUMER_KEY = os.getenv("CONSUMER_KEY")
    CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

    return OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
