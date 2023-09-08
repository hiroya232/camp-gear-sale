import requests
from api import POST_TWEET_ENDPOINT, TWITTER_AUTH

from product import get_product_info


def create_content(discount_rate, product_title, short_url):
    return {
        "text": f"""
【{discount_rate}%オフ！】

{product_title}

詳細は🔽からチェック✔
{short_url}

#キャンプ
#アウトドア
#キャンプ好きと繋がりたい
        """
    }


def post_tweet():
    discount_rate, product_title, short_url = get_product_info()

    content = create_content(
        discount_rate,
        product_title,
        short_url,
    )

    response = requests.post(POST_TWEET_ENDPOINT, auth=TWITTER_AUTH, json=content)
    print(response.json())
