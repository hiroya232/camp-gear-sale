from abc import ABC, abstractmethod

from domain.product import Product
from paapi5_python_sdk.api.default_api import DefaultApi


class ProductService(ABC):

    @abstractmethod
    def auth_amazon_api(self) -> DefaultApi:
        raise NotImplementedError

    @abstractmethod
    def fetch_sale_product(self, associate_id: str) -> Product:
        raise NotImplementedError