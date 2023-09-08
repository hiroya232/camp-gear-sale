import sys
import json
from dotenv import load_dotenv


from scheduler import create_scheduler, start_scheduler
from tweet import post_tweet
from product import get_asin_and_short_url_list


load_dotenv()


def main():
    with open(sys.argv[1], "r") as input_json:
        input_data_list = json.load(input_json)

    for input_data in input_data_list:
        target_date = input_data["date"]

        asin_list, short_url_list = get_asin_and_short_url_list(input_data["url_list"])

        create_scheduler(asin_list, short_url_list, target_date, post_tweet)

    start_scheduler(asin_list, short_url_list, target_date, post_tweet)


if __name__ == "__main__":
    main()
