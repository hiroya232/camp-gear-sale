from dataclasses import dataclass


@dataclass(init=True, frozen=True)
class Product:
    """商品の値オブジェクト

    Attributes:
        title (str): 商品タイトル
        brand (str): ブランド名
        full_url (str): 商品のURL
        short_url (str): 商品の短縮URL
        discount_rate (int): 割引率
        discount_amount (int): 割引金額
        image (bytes): 商品画像のバイナリデータ
    """

    title: str
    brand: str
    full_url: str
    short_url: str
    discount_rate: int
    discount_amount: int
    image: bytes
