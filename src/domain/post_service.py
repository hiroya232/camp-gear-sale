from abc import ABC, abstractmethod

from requests_oauthlib import OAuth1


class PostService(ABC):

    @abstractmethod
    def auth_twitter_api(self) -> OAuth1:
        raise NotImplementedError

    @abstractmethod
    def fetch_media_id(
        self, auth: OAuth1, media_upload_endpoint: str, image: bytes
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def post_to_x(self, content: str, image: bytes) -> None:
        raise NotImplementedError

    @abstractmethod
    def post_to_threads(self, content: str) -> None:
        raise NotImplementedError
