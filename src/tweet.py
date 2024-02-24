import logging
import requests

from api import auth_twitter_api, POST_TWEET_ENDPOINT
from product import get_product_info


def create_content(discount_rate, discount_amount, product_title, short_url):
    return {
        "text": f"""
【{discount_rate}%({discount_amount}円)オフ！】

{product_title}

詳細は🔽からチェック✔
{short_url}

#キャンプ
#アウトドア
#キャンプ好きと繋がりたい
        """
    }


def post_tweet():
    TWITTER_AUTH = auth_twitter_api()

    discount_rate, discount_amount, product_title, short_url = get_product_info()

    content = create_content(
        discount_rate,
        discount_amount,
        product_title,
        short_url,
    )

    response = requests.post(POST_TWEET_ENDPOINT, auth=TWITTER_AUTH, json=content)
    print(response.json())
