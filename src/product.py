import random
import re

from pyshorteners import Shortener

shortener = Shortener()

BROWSE_NODE_LIST = [
    "15325701",  # キャンプ用グリル・焚火台
    "15325661",  # クッキング・BBQツール
    "14916981",  # 食器・カトラリー
    "15325651",  # クッカー・ダッチオーブン
    "15347701",  # コンロアクセサリ
    "14917031",  # 燃料
    "15347691",  # シングルバーナー
    "15348671",  # 火起こし
    "15347711",  # ツーバーナー
    "14916931",  # クーラーボックス
    "15325741",  # 保冷剤
    "15348131",  # ジャグ
    "15348141",  # ポリタンク・ウォータータンク
    "15325961",  # フラスコ・スキットル
    "16397403051",  # 浄水器・酸素
    "15325901",  # テーブル
    "15325891",  # チェア
    "2201154051",  # チェア・テーブルアクセサリー
    "15326031",  # ハンモック
    "15325791",  # タープ
    "15325801",  # テント本体
    "15325811",  # テントアクセサリ
    "14916951",  # 寝袋・シュラフ
    "2201147051",  # 折りたたみ式ベッド
    "15326071",  # エアーマット・エアーベッド
    "15326231",  # ピロー(枕)
    "15326251",  # バッグ・アクセサリ
    "10504409051",  # 自動膨張式スリーピングマット
    "10504410051",  # フォームスリーピングマット
    "386606011",  # ヘッドライト
    "14917021",  # ランタン
    "15326141",  # ランタン用アクセサリ
    "15314301",  # ナイフ・マルチツール
    "15326451",  # フォールディングナイフ
    "386599011",  # キャリーカート
    "15348681",  # ストーブ・ヒーター・ウォーマー
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
        product_list = amazon_api.search_items(
            browse_node_id=BROWSE_NODE_LIST[target_browse_node_index],
            item_page=target_page,
            item_count=10,
        )["data"]

        discounted_product_list = [
            product
            for product in product_list
            if product.offers.listings[0].price.savings is not None
            and product.offers.listings[0].price.savings.percentage is not None
            and product.item_info.by_line_info.brand.display_value is not None
        ]
        discounted_product_count = len(discounted_product_list)
        if discounted_product_count > 0:
            discounted_product = discounted_product_list[
                random.randint(0, discounted_product_count - 1)
            ]
            is_found = not is_found

    product_title = discounted_product.item_info.title.display_value
    discount_rate = discounted_product.offers.listings[0].price.savings.percentage
    short_url = shortener.tinyurl.short(discounted_product.detail_page_url)
    brand = discounted_product.item_info.by_line_info.brand.display_value

    product_title = hashtagging_brand_names_in_product_titie(product_title, brand)
    product_title = omit_product_title(product_title)

    return discount_rate, product_title, short_url
