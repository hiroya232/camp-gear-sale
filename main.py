import sys
import json
import datetime
import re
import time
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
ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
ASSOCIATE_ID = os.getenv('ASSOCIATE_ID')
COUNTRY = 'JP'

AMAZON_API = AmazonAPI(ACCESS_KEY, SECRET_KEY, ASSOCIATE_ID, COUNTRY )


# TwitterAPI情報
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

TWITTER_AUTH = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
TWITTER_API_URL = 'https://api.twitter.com/2/tweets'

scheduler_list = {}
target_product_idx_list = {}


def extract_asin_from_url(url):
  # 通常の商品ページのURLからASINを抽出
  match = re.search(r'/dp/(\w{10})', url)
  if match:
      return match.group(1)

  # 別の形式のURLからASINを抽出
  match = re.search(r'/gp/product/(\w{10})', url)
  if match:
      return match.group(1)

  return None


def post_tweet(asin_list, shortened_url_list, scheduler_name):
  global target_product_idx_list

  target_product_asin = asin_list[target_product_idx_list[scheduler_name]]

  product_data = AMAZON_API.get_items(item_ids=[target_product_asin])['data'][target_product_asin]

  product_title         = product_data.item_info.title.display_value
  product_discount_rate = product_data.offers.listings[0].price.savings.percentage

  product_brand               = product_data.item_info.by_line_info.brand.display_value
  product_brand_notation_list = re.split('[()]', product_brand)[:-1]
  for product_brand_notation in product_brand_notation_list:
    if " " in product_brand_notation:
      product_brand_notation_without_white_space = product_brand_notation.replace(' ', '')
      product_brand_notation_with_hashtag = '#' + product_brand_notation_without_white_space + ' '
    else:
      product_brand_notation_with_hashtag = '#' + product_brand_notation + ' '

    product_title = product_title.replace(product_brand_notation, product_brand_notation_with_hashtag)

  if len(product_title) >= 60:
     product_title = product_title[:60] + '…'

  payload = {
    'text': f"""
【{product_discount_rate}%オフ！】

{product_title}

詳細は🔽からチェック✔
{shortened_url_list[target_product_idx_list[scheduler_name]]}

#キャンプ
#アウトドア
#キャンプ好きと繋がりたい
    """
  }

  response = requests.post(TWITTER_API_URL, auth=TWITTER_AUTH, json=payload)

  print(response.json())

  target_product_idx_list[scheduler_name] += 1
  if target_product_idx_list[scheduler_name] >= len(asin_list):
     return scheduler_name


def job_listener(event: JobExecutionEvent):
  finished_scheduler_name = event.retval
  if finished_scheduler_name is not None:
    scheduler_list[finished_scheduler_name].shutdown(wait=True)


def main():
  shortener = Shortener()

  for index, arg in enumerate(sys.argv):
    if index != 0:
      persed_arg = (json.loads(arg))

      url_list   = persed_arg['url_list']
      asin_list          = []
      shortened_url_list = []
      for url in url_list:
        asin_list.append(extract_asin_from_url(url))
        shortened_url_list.append(shortener.tinyurl.short(url))

      scheduler_name = persed_arg['date']
      scheduler_list[scheduler_name] = BlockingScheduler(timezone='Asia/Tokyo')
      scheduler_list[scheduler_name].add_listener(job_listener, EVENT_JOB_EXECUTED)
      target_product_idx_list[scheduler_name] = 0

      scheduler_list[scheduler_name].add_job(post_tweet, 'interval', seconds=3, args=[asin_list, shortened_url_list, scheduler_name])

  for key, scheduler in scheduler_list.items():
    exec_datetime = datetime.datetime.strptime(key, '%Y-%m-%d')
    now_datetime = datetime.datetime.now()
    if exec_datetime.date() == now_datetime.date():
      scheduler.start()
    else:
      delta = exec_datetime.replace(hour=7, minute=0, second=0) - now_datetime
      time.sleep(delta.total_seconds())
      scheduler.start()

if __name__ == '__main__':
    main()
