from dataclasses import dataclass
import re


@dataclass(init=False, frozen=False)
class Post:

    content: str
    media: bytes

    POST_MAX_LENGTH = 140
    POST_TEMPLATE_LENGTH = 63  # 固定の文字列 + 三点リーダ「…」の合計文字数

    def calculate_excess_length(self, dynamic_content_list):
        dynamic_contents_length = sum(len(el) for el in dynamic_content_list)
        post_length = self.POST_TEMPLATE_LENGTH + dynamic_contents_length

        excess_length = 0
        if post_length > self.POST_MAX_LENGTH:
            excess_length = post_length - self.POST_MAX_LENGTH
            return excess_length

        return excess_length

    def add_hashtags(self, input_text, hashtag_targets):
        brand_notation_list = re.split("[()]", hashtag_targets)
        for brand_notation in brand_notation_list:
            if brand_notation == "":
                continue
            elif " " in brand_notation:
                brand_notation_without_white_space = brand_notation.replace(" ", "")
                brand_notation_with_hashtag = (
                    "#" + brand_notation_without_white_space + " "
                )
                brand_notation = brand_notation.replace(" ", " ?")
            else:
                brand_notation_with_hashtag = "#" + brand_notation + " "

            hashtagged_text = re.sub(
                brand_notation,
                brand_notation_with_hashtag,
                input_text,
                flags=re.IGNORECASE,
            )

        return hashtagged_text

    def shorten_content(self, target_content, shorten_length):
        return target_content[:-shorten_length] + "…"

    def create_content(self, dynamic_content_list):
        return f"""
🏷️ {dynamic_content_list[0]}%🈹 {dynamic_content_list[1]}円オフ！ 🏷️

{dynamic_content_list[2]}

詳細は下記リンクからチェック☑️
{dynamic_content_list[3]}

#キャンプ
#アウトドア
#キャンプ好きと繋がりたい
            """

    def create_post(self, content, media_id):
        return {"text": content, "media": {"media_ids": [media_id]}}
