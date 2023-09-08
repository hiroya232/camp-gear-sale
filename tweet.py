import requests
from api import POST_TWEET_ENDPOINT, TWITTER_AUTH

from product import get_product_info
from scheduler import finished_scheduler, target_product_index_list


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


def post_tweet(asin_list, short_url_list, target_date):
    global target_product_index_list

    discount_rate, product_title = get_product_info(
        asin_list[target_product_index_list[target_date]]
    )

    content = create_content(
        discount_rate,
        product_title,
        short_url_list[target_product_index_list[target_date]],
    )

    response = requests.post(POST_TWEET_ENDPOINT, auth=TWITTER_AUTH, json=content)
    print(response.json())

    return finished_scheduler(target_date, asin_list)
