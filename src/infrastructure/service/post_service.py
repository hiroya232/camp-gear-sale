import os

import requests
from requests_oauthlib import OAuth1

from domain.post import Post
from domain.post_service import PostService
from infrastructure.const import MEDIA_UPLOAD_ENDPOINT, POST_TWEET_ENDPOINT
from logger_config import logger


class PostService(PostService):

    def auth_twitter_api(self) -> OAuth1:
        """XAPIの認証情報を取得する

        Returns:
            OAuth1: XAPIの認証情報
        """
        return OAuth1(
            os.environ["CONSUMER_KEY"],
            os.environ["CONSUMER_SECRET"],
            os.environ["ACCESS_TOKEN"],
            os.environ["ACCESS_TOKEN_SECRET"],
        )

    def fetch_media_id(
        self, auth: OAuth1, media_upload_endpoint: str, image: bytes
    ) -> str:
        """Xに画像をアップロードし、メディアIDを取得する

        Args:
            auth (OAuth1): XAPIの認証情報
            media_upload_endpoint (str): メディアアップロードエンドポイント
            image (bytes): 画像のバイナリデータ

        Returns:
            str: XにアップロードされたメディアのID
        """
        return requests.post(
            media_upload_endpoint, auth=auth, files={"media": image}
        ).json()["media_id_string"]

    def post_to_x(self, content: str, image: bytes) -> None:
        """Xにポストを投稿する

        Args:
            content (str): 投稿内容
            image (bytes): 画像のバイナリデータ

        Raises:
            requests.exceptions.HTTPError: レートリミットに達した場合
            requests.exceptions.RequestException: リクエスト中にエラーが発生した場合
            Exception: 予期せぬエラーが発生した場合
        """
        post = Post()

        auth = self.auth_twitter_api()
        media_id = self.fetch_media_id(auth, MEDIA_UPLOAD_ENDPOINT, image)
        x_post_payload = post.create_x_post_payload(content, media_id)

        try:
            x_response = requests.post(
                POST_TWEET_ENDPOINT, auth=auth, json=x_post_payload
            )
            logger.info(
                "【X API】メディアコンテナ作成リクエストのレスポンス : %s",
                x_response.json(),
            )

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                logger.error(
                    f"レート上限に達しました。: {e}",
                    exc_info=True,
                )
        except requests.exceptions.RequestException as e:
            logger.error(
                f"リクエスト中にエラーが発生しました。: {e}",
                exc_info=True,
            )
        except Exception as e:
            logger.error(
                f"投稿中に予期せぬエラーが発生しました。: {e}",
                exc_info=True,
            )

    def post_to_threads(self, content: str) -> None:
        """Threadsにポストを投稿する

        Args:
            content (str): 投稿内容

        Raises:
            requests.exceptions.HTTPError: レートリミットに達した場合
            requests.exceptions.RequestException: リクエスト中にエラーが発生した場合
            Exception: 予期せぬエラーが発生した場合
        """
        post = Post()

        threads_auth = "Bearer " + os.environ["THREADS_ACCESS_TOKEN"]
        threads_post_payload = post.create_threads_post_payload(content)

        try:
            threads_response = requests.post(
                "https://graph.threads.net/v1.0/me/threads",
                json=threads_post_payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": threads_auth,
                },
            )
            logger.info(
                "【Threads API】メディアコンテナ作成リクエストのレスポンス : %s",
                threads_response.json(),
            )

            threads_response = requests.post(
                "https://graph.threads.net/v1.0/me/threads_publish",
                json={"creation_id": threads_response.json()["id"]},
                headers={
                    "Content-Type": "application/json",
                    "Authorization": threads_auth,
                },
            )
            logger.info(
                "【Threads API】メディアコンテナ公開リクエストのレスポンス : %s",
                threads_response.json(),
            )
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                logger.error(
                    f"レート上限に達しました。: {e}",
                    exc_info=True,
                )
        except requests.exceptions.RequestException as e:
            logger.error(
                f"リクエスト中にエラーが発生しました。: {e}",
                exc_info=True,
            )
        except Exception as e:
            logger.error(
                f"投稿中に予期せぬエラーが発生しました。: {e}",
                exc_info=True,
            )
