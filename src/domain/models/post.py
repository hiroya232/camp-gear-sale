import re
from dataclasses import dataclass
from textwrap import dedent


@dataclass(init=False, frozen=True)
class Post:
    """ポストの値オブジェクト

    Attributes:
        content (str): ポストの本文
        media (bytes): 添付画像のバイナリデータ

    Constants:
        POST_MAX_LENGTH (int): ポストの最大文字数
        POST_TEMPLATE_LENGTH (int): ポストの固定文字列と三点リーダ「…」の合計文字数
    """

    content: str
    media: bytes

    POST_MAX_LENGTH = 140
    POST_TEMPLATE_LENGTH = 63  # 固定の文字列 + 三点リーダ「…」の合計文字数

    def calculate_excess_length(self, dynamic_content_list: list) -> int:
        """本文の文字数が規定文字数を超過している場合の超過文字数を計算する

        Args:
            dynamic_content_list (list): 動的コンテンツのリスト

        Returns:
            int: 超過文字数
        """
        dynamic_contents_length = sum(len(el) for el in dynamic_content_list)
        post_length = self.POST_TEMPLATE_LENGTH + dynamic_contents_length

        if post_length > self.POST_MAX_LENGTH:
            return post_length - self.POST_MAX_LENGTH

        return 0

    def add_hashtags(self, target_text: str, hashtag_target: str) -> str:
        """本文にハッシュタグを追加する

        Args:
            target_text (str): 置換対象の本文
            hashtag_target (str): ハッシュタグ化対象の文字列

        Returns:
            str: 対象文字列をハッシュタグ化した本文
        """
        return re.sub(
            re.escape(hashtag_target),
            "#" + hashtag_target.replace(" ", "") + " ",
            target_text,
            flags=re.IGNORECASE,
        )

    def shorten_content(self, target_content: str, shorten_length: int) -> str:
        """本文を指定文字数に短縮する

        Args:
            target_content (str): 短縮対象の本文
            shorten_length (int): 短縮する文字数

        Returns:
            str: _description_
        """
        return target_content[:-shorten_length] + "…"

    def create_content(self, dynamic_content_list: list) -> str:
        """本文を生成する

        Args:
            dynamic_content_list (list): 動的コンテンツのリスト

        Returns:
            str: 生成された本文
        """
        return dedent(
            f"""
                🏷️ {dynamic_content_list[0]}%🈹 {dynamic_content_list[1]}円オフ！ 🏷️

                {dynamic_content_list[2]}

                詳細は下記リンクからチェック☑️
                {dynamic_content_list[3]}

                #キャンプ
                #アウトドア
                #キャンプ好きと繋がりたい
            """
        )

    def create_x_post_payload(self, content: str, media_id: str) -> dict:
        """XAPIへのポストリクエストのペイロードを生成する

        Args:
            content (str): ポストの本文
            media_id (str): 添付画像のメディアID

        Returns:
            dict: 生成されたペイロード
        """
        return {"text": content, "media": {"media_ids": [media_id]}}

    def create_threads_post_payload(self, content: str) -> dict:
        """ThreadsAPIへのポストリクエストのペイロードを生成する

        Args:
            content (str): ポストの本文

        Returns:
            dict: 生成されたペイロード
        """
        return {
            "media_type": "TEXT",
            "text": content,
        }
