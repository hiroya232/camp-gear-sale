import sys
sys.path.append("src")

from dotenv import load_dotenv

from scheduler import add_job, start_scheduler
from tweet import post_tweet


def main():
    load_dotenv()

    add_job(post_tweet)

    start_scheduler(post_tweet)


if __name__ == "__main__":
    main()
