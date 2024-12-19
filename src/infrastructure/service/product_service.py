import os
import random
import time

import requests
from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.models.partner_type import PartnerType
from paapi5_python_sdk.models.search_items_request import SearchItemsRequest
from paapi5_python_sdk.models.search_items_resource import SearchItemsResource
from paapi5_python_sdk.rest import ApiException

from domain.product import Product
from domain.product_service import ProductService
from infrastructure.const import BROWSE_NODE_LIST
from infrastructure.dto.raw_product_data import RawProductData
from logger_config import logger


class ProductService(ProductService):

    def auth_amazon_api(self) -> DefaultApi:
        """Amazon APIの認証情報を取得する

        Returns:
            DefaultApi: Amazon APIの認証情報
        """
        return DefaultApi(
            access_key=os.environ["ACCESS_KEY"],
            secret_key=os.environ["SECRET_KEY"],
            host=os.environ["HOST"],
            region=os.environ["REGION"],
        )

    def fetch_sale_product(self, associate_id: str) -> Product:
        """セール商品を取得する

        Args:
            associate_id (str): アソシエイトID

        Returns:
            Product: 商品情報

        Raises:
            ApiException: APIリクエスト時にエラーが発生した場合
            AttributeError: 取得した商品情報に必要なデータが含まれていない場合
            Exception: 予期せぬエラーが発生した場合
        """
        amazon_api = self.auth_amazon_api()

        is_found = False
        while not is_found:
            target_browse_node_index = random.randint(0, len(BROWSE_NODE_LIST) - 1)
            target_page = random.randint(1, 10)

            try:
                sale_product_list = amazon_api.search_items(
                    SearchItemsRequest(
                        partner_tag=associate_id,
                        partner_type=PartnerType.ASSOCIATES,
                        browse_node_id=BROWSE_NODE_LIST[target_browse_node_index],
                        delivery_flags=["Prime"],
                        item_page=target_page,
                        item_count=10,
                        min_saving_percent=1,
                        resources=[
                            SearchItemsResource.ITEMINFO_TITLE,
                            SearchItemsResource.ITEMINFO_BYLINEINFO,
                            SearchItemsResource.OFFERS_LISTINGS_PRICE,
                            SearchItemsResource.IMAGES_PRIMARY_LARGE,
                        ],
                    )
                ).search_result.items

                sale_product_list = [
                    sale_product
                    for sale_product in sale_product_list
                    if sale_product.offers.listings[0].price.savings is not None
                    and sale_product.offers.listings[0].price.savings.percentage
                    is not None
                    and sale_product.offers.listings[0].price.savings.amount is not None
                    and sale_product.item_info.by_line_info.brand.display_value
                    is not None
                ]

                sale_product_count = len(sale_product_list)
                if sale_product_count > 0:
                    sale_product = sale_product_list[
                        random.randint(0, sale_product_count - 1)
                    ]
                    is_found = not is_found
                    logger.info("選択した商品情報 : %s", sale_product)
            except ApiException as e:
                logger.error(
                    f"PA-APIへのリクエスト時にエラーが発生しました。: {e}",
                    exc_info=True,
                )
            except AttributeError as e:
                logger.error(
                    f"取得した商品情報に必要なデータが含まれていません。: {e}",
                    exc_info=True,
                )
                continue
            except Exception as e:
                logger.error(
                    f"セール商品取得中に予期せぬエラーが発生しました。: {e}",
                    exc_info=True,
                )
                continue
            finally:
                time.sleep(1)

        return RawProductData(
            title=sale_product.item_info.title.display_value,
            brand=sale_product.item_info.by_line_info.brand.display_value,
            full_url=sale_product.detail_page_url,
            short_url="",
            discount_rate=sale_product.offers.listings[0].price.savings.percentage,
            discount_amount=round(sale_product.offers.listings[0].price.savings.amount),
            image=requests.get(sale_product.images.primary.large.url).content,
        )
