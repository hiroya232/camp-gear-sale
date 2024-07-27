import os
import random

from amazon_paapi import AmazonApi
import requests

from domain.product import Product


class ProductService:

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

    def auth_amazon_api(self):
        ACCESS_KEY = os.getenv("ACCESS_KEY")
        SECRET_KEY = os.getenv("SECRET_KEY")
        ASSOCIATE_ID = os.getenv("ASSOCIATE_ID")
        COUNTRY = "JP"

        return AmazonApi(ACCESS_KEY, SECRET_KEY, ASSOCIATE_ID, COUNTRY)

    def fetch_sale_product(self):
        amazon_api = self.auth_amazon_api()

        is_found = False
        while not is_found:
            target_browse_node_index = random.randint(0, len(self.BROWSE_NODE_LIST) - 1)
            target_page = random.randint(1, 10)
            sale_product_list = amazon_api.search_items(
                browse_node_id=self.BROWSE_NODE_LIST[target_browse_node_index],
                item_page=target_page,
                item_count=10,
                min_saving_percent=1,
            ).items

            sale_product_list = [
                sale_product
                for sale_product in sale_product_list
                if sale_product.offers.listings[0].price.savings is not None
                and sale_product.offers.listings[0].price.savings.percentage is not None
                and sale_product.offers.listings[0].price.savings.amount is not None
                and sale_product.item_info.by_line_info.brand.display_value is not None
            ]

            sale_product_count = len(sale_product_list)
            if sale_product_count > 0:
                sale_product = sale_product_list[
                    random.randint(0, sale_product_count - 1)
                ]
                is_found = not is_found

        return Product(
            title=sale_product.item_info.title.display_value,
            brand=sale_product.item_info.by_line_info.brand.display_value,
            full_url=sale_product.detail_page_url,
            short_url="",
            discount_rate=sale_product.offers.listings[0].price.savings.percentage,
            discount_amount=round(sale_product.offers.listings[0].price.savings.amount),
            image=requests.get(sale_product.images.primary.large.url).content,
        )
