import re

from pyshorteners import Shortener
from api import AMAZON_API

shortener = Shortener()


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


def get_asin_and_short_url_list(url_list):
    asin_list = []
    short_url_list = []
    for url in url_list:
        asin_list.append(extract_asin_from_url(url))
        short_url_list.append(shortener.tinyurl.short(url))

    return asin_list, short_url_list


def hashtagging_brand_names_in_product_titie(product_title, brand):
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

    return product_title


def omit_product_title(product_title):
    if len(product_title) >= 60:
        product_title = product_title[:60] + "…"

    return product_title


def get_product_info(target_product_asin):
    product_data = AMAZON_API.get_items(item_ids=[target_product_asin])["data"][
        target_product_asin
    ]

    product_title = product_data.item_info.title.display_value
    discount_rate = product_data.offers.listings[0].price.savings.percentage
    brand = product_data.item_info.by_line_info.brand.display_value

    product_title = hashtagging_brand_names_in_product_titie(product_title, brand)
    product_title = omit_product_title(product_title)

    return discount_rate, product_title
