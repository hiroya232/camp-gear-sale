import requests
from requests.exceptions import RequestException

from api import POST_TWEET_ENDPOINT

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


def post_tweet(amazon_api, twitter_auth):
    discount_rate, product_title, short_url = get_product_info(amazon_api)

    content = create_content(
        discount_rate,
        product_title,
        short_url,
    )

    try:
        response = requests.post(POST_TWEET_ENDPOINT, auth=twitter_auth, json=content)
        print(response.json())
    except RequestException as e:
        logging.error(f"Twitter API Request failed: {e}")
