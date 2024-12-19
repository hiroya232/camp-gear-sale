import os
import re

from pyshorteners import Shortener

from domain.models.post import Post
from domain.interfaces.post_service import PostService
from domain.models.product import Product
from domain.interfaces.product_service import ProductService


class PostCampGearSaleUseCase:

    def __init__(
        self, product_service: ProductService, post_service: PostService
    ) -> None:
        self.product_service = product_service
        self.post_service = post_service

    def handle(self) -> None:

        post = Post()
        shortener = Shortener()

        associate_ids = {
            "x": os.environ["X_ASSOCIATE_ID"],
            "threads": os.environ["THREADS_ASSOCIATE_ID"],
        }

        for key, associate_id in associate_ids.items():
            raw_product_data = self.product_service.fetch_sale_product(associate_id)

            brand_notation_list = [
                bn for bn in re.split(r"\((.*?)\)", raw_product_data.brand) if bn != ""
            ]
            brand_notation_list += [
                bn.replace(" ", "") for bn in brand_notation_list if " " in bn
            ]

            for bn in brand_notation_list:
                raw_product_data.title = post.add_hashtags(raw_product_data.title, bn)
            raw_product_data.title = raw_product_data.title.replace("##", "#")

            raw_product_data.short_url = shortener.tinyurl.short(
                raw_product_data.full_url
            )

            excess_length = post.calculate_excess_length(
                [
                    raw_product_data.title,
                    str(raw_product_data.discount_rate),
                    str(raw_product_data.discount_amount),
                    raw_product_data.short_url,
                ]
            )
            if excess_length > 0:
                raw_product_data.title = post.shorten_content(
                    raw_product_data.title, excess_length
                )

            product = Product(
                title=raw_product_data.title,
                brand=raw_product_data.brand,
                full_url=raw_product_data.full_url,
                short_url=raw_product_data.short_url,
                discount_rate=raw_product_data.discount_rate,
                discount_amount=raw_product_data.discount_amount,
                image=raw_product_data.image,
            )

            post_content = post.create_content(
                [
                    product.discount_rate,
                    product.discount_amount,
                    product.title,
                    product.short_url,
                ]
            )

            if key == "x":
                self.post_service.post_to_x(post_content, product.image)
            elif key == "threads":
                self.post_service.post_to_threads(post_content)
            else:
                continue
