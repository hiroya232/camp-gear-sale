import logging
import os

from requests_oauthlib import OAuth1
import requests

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
        x_post_payload = post.create_x_post_payload(content, media_id)

        threads_auth = "Bearer " + os.environ["THREADS_ACCESS_TOKEN"]
        threads_post_payload = post.create_threads_post_payload(content)

        try:
            x_response = requests.post(
                self.POST_TWEET_ENDPOINT, auth=auth, json=x_post_payload
            )
            print(x_response.json())

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
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                logging.error(
                    f"レート上限に達しました。: {e}",
                    exc_info=True,
                )
        except requests.exceptions.RequestException as e:
            logging.error(
                f"リクエスト中にエラーが発生しました。: {e}",
                exc_info=True,
            )
        except Exception as e:
            logging.error(
                f"投稿中に予期せぬエラーが発生しました。: {e}",
                exc_info=True,
            )
