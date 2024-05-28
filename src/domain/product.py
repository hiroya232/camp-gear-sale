from dataclasses import dataclass


@dataclass(init=True, frozen=False)
class Product:

    title: str
    brand: str
    full_url: str
    short_url: str
    discount_rate: int
    discount_amount: int
    image: bytes
