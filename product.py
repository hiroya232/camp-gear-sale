import random
import re

from pyshorteners import Shortener

shortener = Shortener()

BROWSE_NODE_LIST = [
    "2201151051",
    "14916931",
    "15325821",
    "14916971",
    "15325791",
    "14916991",
    "14917011",
    "15325991",
    "14917001",
]


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


def get_product_info(amazon_api):
    is_found = False
    while not is_found:
        target_browse_node_index = random.randint(0, len(BROWSE_NODE_LIST) - 1)
        target_page = random.randint(1, 10)

        product_data = amazon_api.search_items(
            browse_node_id=BROWSE_NODE_LIST[target_browse_node_index],
            item_page=target_page,
            item_count=1,
        )["data"][0]

        if product_data.offers.listings[0].price.savings is not None:
            is_found = not is_found

    product_title = product_data.item_info.title.display_value
    discount_rate = product_data.offers.listings[0].price.savings.percentage
    short_url = shortener.tinyurl.short(product_data.detail_page_url)
    brand = product_data.item_info.by_line_info.brand.display_value

    product_title = hashtagging_brand_names_in_product_titie(product_title, brand)
    product_title = omit_product_title(product_title)

    return discount_rate, product_title, short_url
