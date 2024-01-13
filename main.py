from dotenv import load_dotenv
import sys

sys.path.append("src")

from api import auth_amazon_api, auth_twitter_api
from scheduler import add_job, start_scheduler
from tweet import post_tweet


def main():
    load_dotenv()

    AMAZON_API = auth_amazon_api()
    TWITTER_AUTH = auth_twitter_api()

    add_job(post_tweet, AMAZON_API, TWITTER_AUTH)

    start_scheduler(post_tweet, AMAZON_API, TWITTER_AUTH)


if __name__ == "__main__":
    main()
