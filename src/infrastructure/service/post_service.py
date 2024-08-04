import os
import requests

from requests_oauthlib import OAuth1

from domain.post import Post


class PostService:

    POST_TWEET_ENDPOINT = "https://api.twitter.com/2/tweets"
    MEDIA_UPLOAD_ENDPOINT = "https://upload.twitter.com/1.1/media/upload.json"

    def auth_twitter_api(self):
        CONSUMER_KEY = os.environ["CONSUMER_KEY"]
        CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
        ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
        ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]

        return OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    def fetch_media_id(self, auth, media_upload_endpoint, image):
        return requests.post(
            media_upload_endpoint, auth=auth, files={"media": image}
        ).json()["media_id_string"]

    def post(self, content, image):

        post = Post()

        auth = self.auth_twitter_api()
        media_id = self.fetch_media_id(auth, self.MEDIA_UPLOAD_ENDPOINT, image)
        post = post.create_post(content, media_id)

        response = requests.post(self.POST_TWEET_ENDPOINT, auth=auth, json=post)
        print(response.json())
