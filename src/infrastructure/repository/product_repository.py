class ProductRepository:

    def __init__(self, product_service):
        self.product_service = product_service

    def fetch_sale_product(self, associate_id):
        return self.product_service.fetch_sale_product(associate_id)
