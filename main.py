import sys
import json
import datetime
import re
import time
from zoneinfo import ZoneInfo
import requests
import os
from dotenv import load_dotenv

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, JobExecutionEvent
from pyshorteners import Shortener
from amazon.paapi import AmazonAPI
from requests_oauthlib import OAuth1

load_dotenv()

# PA-API情報
ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
ASSOCIATE_ID = os.getenv("ASSOCIATE_ID")
COUNTRY = "JP"

AMAZON_API = AmazonAPI(ACCESS_KEY, SECRET_KEY, ASSOCIATE_ID, COUNTRY)


# TwitterAPI情報
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

TWITTER_AUTH = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
POST_TWEET_ENDPOINT = "https://api.twitter.com/2/tweets"

scheduler_list = {}
target_product_index_list = {}


def extract_asin_from_url(url):
    # 通常の商品ページのURLからASINを抽出
    match = re.search(r"/dp/(\w{10})", url)
    if match:
        return match.group(1)

    # 別の形式のURLからASINを抽出
    match = re.search(r"/gp/product/(\w{10})", url)
    if match:
        return match.group(1)

    return None


def post_tweet(asin_list, short_url_list, target_date):
    global target_product_index_list

    target_product_asin = asin_list[target_product_index_list[target_date]]

    product_data = AMAZON_API.get_items(item_ids=[target_product_asin])["data"][
        target_product_asin
    ]

    product_title = product_data.item_info.title.display_value
    discount_rate = product_data.offers.listings[0].price.savings.percentage

    brand = product_data.item_info.by_line_info.brand.display_value
    brand_notation_list = re.split("[()]", brand)
    for brand_notation in brand_notation_list:
        if brand_notation == "":
            continue
        elif " " in brand_notation:
            brand_notation_without_white_space = brand_notation.replace(" ", "")
            brand_notation_with_hashtag = "#" + brand_notation_without_white_space + " "
            brand_notation = brand_notation.replace(" ", " ?")
        else:
            brand_notation_with_hashtag = "#" + brand_notation + " "

        product_title = re.sub(
            brand_notation,
            brand_notation_with_hashtag,
            product_title,
            flags=re.IGNORECASE,
        )

    if len(product_title) >= 60:
        product_title = product_title[:60] + "…"

    payload = {
        "text": f"""
【{discount_rate}%オフ！】

{product_title}

詳細は🔽からチェック✔
{short_url_list[target_product_index_list[target_date]]}

#キャンプ
#アウトドア
#キャンプ好きと繋がりたい
    """
    }

    response = requests.post(POST_TWEET_ENDPOINT, auth=TWITTER_AUTH, json=payload)

    print(response.json())

    target_product_index_list[target_date] += 1
    if target_product_index_list[target_date] >= len(asin_list):
        return target_date


def completed_scheduler_listener(event: JobExecutionEvent):
    completed_scheduler = event.retval
    if completed_scheduler is not None:
        scheduler_list[completed_scheduler].shutdown(wait=True)


def main():
    shortener = Shortener()

    with open(sys.argv[1], "r") as input_json:
        input_data_list = json.load(input_json)

    for input_data in input_data_list:
        url_list = input_data["url_list"]
        asin_list = []
        short_url_list = []
        for url in url_list:
            asin_list.append(extract_asin_from_url(url))
            short_url_list.append(shortener.tinyurl.short(url))

        target_date = input_data["date"]
        scheduler_list[target_date] = BlockingScheduler(timezone="Asia/Tokyo")
        scheduler_list[target_date].add_listener(
            completed_scheduler_listener, EVENT_JOB_EXECUTED
        )
        target_product_index_list[target_date] = 0

        scheduler_list[target_date].add_job(
            post_tweet,
            "interval",
            hours=1,
            args=[asin_list, short_url_list, target_date],
        )

    for date, scheduler in scheduler_list.items():
        exec_date = datetime.datetime.strptime(date, "%Y-%m-%d").astimezone(
            ZoneInfo("Asia/Tokyo")
        )
        now_datetime = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
        if exec_date.date() == now_datetime.date():
            post_tweet(asin_list, short_url_list, target_date)
            scheduler.start()
        else:
            delta = exec_date.replace(hour=7, minute=0, second=0) - now_datetime
            time.sleep(delta.total_seconds())
            scheduler.start()


if __name__ == "__main__":
    main()
