from dataclasses import dataclass
from textwrap import dedent


@dataclass(init=False, frozen=False)
class Post:

    content: str
    media: bytes

    POST_MAX_LENGTH = 140
    POST_TEMPLATE_LENGTH = 63  # 固定の文字列 + 三点リーダ「…」の合計文字数

    def calculate_excess_length(self, dynamic_content_list):
        dynamic_contents_length = sum(len(el) for el in dynamic_content_list)
        post_length = self.POST_TEMPLATE_LENGTH + dynamic_contents_length

        if post_length > self.POST_MAX_LENGTH:
            return post_length - self.POST_MAX_LENGTH

        return 0

    def add_hashtags(self, target_text, hashtag_target):
        return target_text.replace(
            hashtag_target,
            "#" + hashtag_target + " ",
        )

    def shorten_content(self, target_content, shorten_length):
        return target_content[:-shorten_length] + "…"

    def create_content(self, dynamic_content_list):
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

    def create_post(self, content, media_id):
        return {"text": content, "media": {"media_ids": [media_id]}}
