from amazon.paapi import AmazonAPI

# PA-API資格情報
ACCESS_KEY = "***REMOVED***" #アクセスキー
SECRET_KEY = "***REMOVED***" #シークレットキー
ASSOCIATE_ID = "***REMOVED***" #アソシエイトID
COUNTRY = "JP"  #日本のAmazonなので"JP"

amazon_api = AmazonAPI(ACCESS_KEY, SECRET_KEY, ASSOCIATE_ID, COUNTRY )

asin_list = [
    [
      'B00QEN7NMU',
      'B00279LZ0G',
      'B09QZ2TXKN',
      'B07HRPBRBS',
      'B07Q7SWXLZ',
      'B0BMPZPSCL',
      'B08563GS15',
      'B09TNDQD56',
      'B08FTBS3HH',
      'B007N77TNO',
      'B07VWGBHZW',
      'B09TNLSN29',
      'B0BQJ18TX5',
      'B073PSRTCG',
      'B000UH0ROM',
      'B0BM46PJ9C',
      'B07X9VZD3M',
    ],
]


# ツイート投稿
import requests
from requests_oauthlib import OAuth1
from apscheduler.schedulers.blocking import BlockingScheduler

# Twitter API資格情報
CONSUMER_KEY = '***REMOVED***'
CONSUMER_SECRET = '***REMOVED***'
ACCESS_TOKEN = '***REMOVED***'
ACCESS_TOKEN_SECRET = '***REMOVED***'

# OAuth1認証
auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Twitter API v2のエンドポイント
endpoint_url = "https://api.twitter.com/2/tweets"

import datetime
import pytz

tokyo_tz = pytz.timezone("Asia/Tokyo")
now_date = datetime.datetime.now(tokyo_tz)  # 現在の日時をAsia/Tokyoのタイムゾーンで取得
print(now_date)

def post_tweet(asin):
  products = amazon_api.get_items(item_ids=[asin])

  product_title = products['data'][asin].item_info.title.display_value
  product_discount_rate = products['data'][asin].offers.listings[0].price.savings.percentage
  product_url = products['data'][asin].detail_page_url

    # ツイート内容の作成
  tweet_content = f"""
【{product_discount_rate}%オフ！】

{product_title}

詳細は🔽からチェック✔
{product_url}

#キャンプ
#アウトドア
#キャンプ好きと繋がりたい
  """

  payload = {
    "text": tweet_content
  }

  print(payload)

  # ツイートの投稿
  response = requests.post(endpoint_url, auth=auth, json=payload)

  # レスポンスを表示
  print(datetime.datetime.now(tokyo_tz))
  print(response.json())


# タスクのスケジュール設定
scheduler = BlockingScheduler(timezone="Asia/Tokyo")

tomorrow_date = now_date + datetime.timedelta(days=1)

tweet_datetime_list = [
    now_date.replace(hour=12, minute=0, second=0),
    now_date.replace(hour=12, minute=30, second=0),
    now_date.replace(hour=13, minute=0, second=0),
    now_date.replace(hour=15, minute=0, second=0),
    now_date.replace(hour=15, minute=30, second=0),
    now_date.replace(hour=16, minute=0, second=0),
    now_date.replace(hour=16, minute=30, second=0),
    now_date.replace(hour=17, minute=0, second=0),
    now_date.replace(hour=20, minute=0, second=0),
    now_date.replace(hour=20, minute=30, second=0),
    now_date.replace(hour=21, minute=0, second=0),
    now_date.replace(hour=21, minute=30, second=0),
    now_date.replace(hour=22, minute=0, second=0),
    now_date.replace(hour=22, minute=30, second=0),
    now_date.replace(day=tomorrow_date.day, hour=7, minute=0, second=0),
    now_date.replace(day=tomorrow_date.day, hour=7, minute=30, second=0),
    now_date.replace(day=tomorrow_date.day, hour=8, minute=0, second=0),
]

for i, asin_daily in enumerate(asin_list):
  for asin, tweet_datetime  in zip(asin_daily, tweet_datetime_list):
    if i != 0:
      tweet_datetime += datetime.timedelta(days=1)
    scheduler.add_job(post_tweet, 'date', run_date=tweet_datetime, args=[asin])

scheduler.start()
