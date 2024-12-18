from dataclasses import dataclass


@dataclass(init=True, frozen=False)
class RawProductData:
    title: str
    brand: str
    full_url: str
    short_url: str
    discount_rate: float
    discount_amount: float
    image: bytes
