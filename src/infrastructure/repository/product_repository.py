class ProductRepository:

    def __init__(self, product_service):
        self.product_service = product_service

    def fetch_product_info(self):
        return self.product_service.fetch_product_info()
