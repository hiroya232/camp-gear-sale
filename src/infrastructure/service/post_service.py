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
        media_id = self.fetch_media_id(
            auth,
            self.MEDIA_UPLOAD_ENDPOINT,
            requests.get(image).content,
        )
        x_post_payload = post.create_x_post_payload(content, media_id)

        x_response = requests.post(
            self.POST_TWEET_ENDPOINT, auth=auth, json=x_post_payload
        )
        print(x_response.json())

        threads_auth = "Bearer " + os.environ["THREADS_ACCESS_TOKEN"]
        threads_post_payload = post.create_threads_post_payload(content)
        threads_response = requests.post(
            "https://graph.threads.net/v1.0/me/threads",
            json=threads_post_payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": threads_auth,
            },
        )
        print(threads_response.json())
        threads_response = requests.post(
            "https://graph.threads.net/v1.0/me/threads_publish",
            json={"creation_id": threads_response.json()["id"]},
            headers={
                "Content-Type": "application/json",
                "Authorization": threads_auth,
            },
        )
        print(threads_response.json())

        instagram_auth = "Bearer " + os.environ["INSTAGRAM_ACCESS_TOKEN"]
        instagram_post_payload = post.create_instagram_post_payload(content, image)
        instagram_response = requests.post(
            "https://graph.instagram.com/v20.0/me/media",
            json=instagram_post_payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": instagram_auth,
            },
        )
        print(instagram_response.json())
        instagram_response = requests.post(
            "https://graph.instagram.com/v20.0/me/media_publish",
            json={"creation_id": instagram_response.json()["id"]},
            headers={
                "Content-Type": "application/json",
                "Authorization": instagram_auth,
            },
        )
        print(instagram_response.json())
