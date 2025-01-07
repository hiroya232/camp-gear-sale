from dataclasses import dataclass


@dataclass(init=True, frozen=False)
class RawProductData:
    """取得した商品情報の生データを保持するDTOクラス

    Attributes:
        title (str): 商品タイトル
        brand (str): ブランド名
        full_url (str): 商品のURL
        short_url (str): 商品の短縮URL
        discount_rate (float): 割引率
        discount_amount (float): 割引額
        image (bytes): 商品画像のバイナリデータ
    """

    title: str
    brand: str
    full_url: str
    short_url: str
    discount_rate: float
    discount_amount: float
    image: bytes
