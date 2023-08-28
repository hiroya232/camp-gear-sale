import sys
import json
import datetime
import re
import requests

from apscheduler.schedulers.blocking import BlockingScheduler
from pyshorteners import Shortener
from amazon.paapi import AmazonAPI
from requests_oauthlib import OAuth1

# PA-API情報
ACCESS_KEY = '***REMOVED***'
SECRET_KEY = '***REMOVED***'
ASSOCIATE_ID = '***REMOVED***'
COUNTRY = 'JP'

AMAZON_API = AmazonAPI(ACCESS_KEY, SECRET_KEY, ASSOCIATE_ID, COUNTRY )


# TwitterAPI情報
# # テスト用
# CONSUMER_KEY = '***REMOVED***'
# CONSUMER_SECRET = '***REMOVED***'
# ACCESS_TOKEN = '***REMOVED***'
# ACCESS_TOKEN_SECRET = '***REMOVED***'

# 本番用
CONSUMER_KEY = '***REMOVED***'
CONSUMER_SECRET = '***REMOVED***'
ACCESS_TOKEN = '***REMOVED***'
ACCESS_TOKEN_SECRET = '***REMOVED***'

TWITTER_AUTH = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
TWITTER_API_URL = 'https://api.twitter.com/2/tweets'


def get_tweet_datetime_list(tweet_datetime):
  return [
    tweet_datetime.replace(hour=7, minute=0, second=0),
    tweet_datetime.replace(hour=7, minute=30, second=0),
    tweet_datetime.replace(hour=8, minute=0, second=0),
    tweet_datetime.replace(hour=12, minute=0, second=0),
    tweet_datetime.replace(hour=12, minute=30, second=0),
    tweet_datetime.replace(hour=13, minute=0, second=0),
    tweet_datetime.replace(hour=15, minute=0, second=0),
    tweet_datetime.replace(hour=15, minute=30, second=0),
    tweet_datetime.replace(hour=16, minute=0, second=0),
    tweet_datetime.replace(hour=16, minute=30, second=0),
    tweet_datetime.replace(hour=17, minute=0, second=0),
    tweet_datetime.replace(hour=20, minute=0, second=0),
    tweet_datetime.replace(hour=20, minute=30, second=0),
    tweet_datetime.replace(hour=21, minute=0, second=0),
    tweet_datetime.replace(hour=21, minute=30, second=0),
    tweet_datetime.replace(hour=22, minute=0, second=0),
  ]


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


def post_tweet(asin, shortened_url):
  product_data = AMAZON_API.get_items(item_ids=[asin])['data'][asin]

  product_title         = product_data.item_info.title.display_value
  product_discount_rate = product_data.offers.listings[0].price.savings.percentage

  product_brand               = product_data.item_info.by_line_info.brand.display_value
  product_brand_notation_list = re.split('[()]', product_brand)[:-1]
  for product_brand_notation in product_brand_notation_list:
    product_brand_notation_with_hashtag = '#' + product_brand_notation + ' '
    product_title = product_title.replace(product_brand_notation, product_brand_notation_with_hashtag)

  if len(product_title) >= 60:
     product_title = product_title[:60] + '…'

  payload = {
    'text': f"""
【{product_discount_rate}%オフ！】

{product_title}

詳細は🔽からチェック✔
{shortened_url}

#キャンプ
#アウトドア
#キャンプ好きと繋がりたい
    """
  }

  response = requests.post(TWITTER_API_URL, auth=TWITTER_AUTH, json=payload)

  print(asin)
  print(response.json())


def main():
  shortener = Shortener()
  scheduler = BlockingScheduler(timezone='Asia/Tokyo')

  for index, arg in enumerate(sys.argv):
    if index != 0:
      persed_arg = (json.loads(arg))
      tweet_date = persed_arg['date']
      url_list   = persed_arg['url_list']

      tweet_datetime = get_tweet_datetime_list(datetime.datetime.strptime(tweet_date, '%Y-%m-%d'))

      asin_list          = []
      shortened_url_list = []
      for url in url_list:
        asin_list.append(extract_asin_from_url(url))
        shortened_url_list.append(shortener.tinyurl.short(url))

      for asin, shortened_url, tweet_datetime in zip(asin_list, shortened_url_list, tweet_datetime):
        if asin is not None:
          scheduler.add_job(post_tweet, 'date', run_date=tweet_datetime, args=[asin, shortened_url])

  scheduler.start()

if __name__ == '__main__':
    main()
