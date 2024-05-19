import requests

from infrastructure.api import auth_twitter_api, POST_TWEET_ENDPOINT, MEDIA_UPLOAD_ENDPOINT
from domain.product import get_product_info, shorten_product_title

POST_MAX_LENGTH = 140
POST_TEMPLATE_TOTAL_LENGTH = 63  # 固定の文字列 + 三点リーダ「…」の合計文字数


def create_content(discount_rate, discount_amount, product_title, short_url):
    product_info_total_length = len(
        str(discount_rate) + str(discount_amount) + product_title + short_url
    )
    post_total_length = POST_TEMPLATE_TOTAL_LENGTH + product_info_total_length

    if post_total_length > POST_MAX_LENGTH:
        excess_length = post_total_length - POST_MAX_LENGTH
        product_title = shorten_product_title(product_title, excess_length)

    return f"""
🏷️ {discount_rate}%🈹 {discount_amount}円オフ！ 🏷️

{product_title}

詳細は下記リンクからチェック☑️
{short_url}

#キャンプ
#アウトドア
#キャンプ好きと繋がりたい
        """


def post_tweet():
    TWITTER_AUTH = auth_twitter_api()

    discount_rate, discount_amount, product_title, short_url, image = get_product_info()

    content = create_content(
        discount_rate,
        discount_amount,
        product_title,
        short_url,
    )

    media_id = requests.post(
        MEDIA_UPLOAD_ENDPOINT, auth=TWITTER_AUTH, files={"media": image}
    ).json()["media_id_string"]
    payload = {"text": content, "media": {"media_ids": [media_id]}}

    response = requests.post(POST_TWEET_ENDPOINT, auth=TWITTER_AUTH, json=payload)
    print(response.json())
