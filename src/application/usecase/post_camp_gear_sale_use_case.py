import re


from pyshorteners import Shortener


from domain.post import Post


class PostCampGearSaleUseCase:

    def __init__(self, product_repository, post_service):
        self.product_repository = product_repository
        self.post_service = post_service

    def handle(self):
        product = self.product_repository.fetch_sale_product()

        brand_notation_list = [
            bn for bn in re.split(r"\((.*?)\)", product.brand) if bn != ""
        ]
        brand_notation_list += [
            bn.replace(" ", "") for bn in brand_notation_list if " " in bn
        ]

        post = Post()

        for bn in brand_notation_list:
            product.title = post.add_hashtags(product.title, bn)

        excess_length = post.calculate_excess_length(
            [
                product.title,
                str(product.discount_rate),
                str(product.discount_amount),
                product.short_url,
            ]
        )
        if excess_length > 0:
            product.title = post.shorten_content(product.title, excess_length)

        shortener = Shortener()
        product.short_url = shortener.tinyurl.short(product.full_url)

        post_content = post.create_content(
            [
                product.discount_rate,
                product.discount_amount,
                product.title,
                product.short_url,
            ]
        )

        self.post_service.post(post_content, product.image)
