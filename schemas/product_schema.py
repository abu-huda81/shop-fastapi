from pydantic import BaseModel
from typing import List, Optional


class ProductImageBase(BaseModel):
    image_url: str


class ProductImageCreate(ProductImageBase):
    pass


class ProductImage(ProductImageBase):
    id: int
    product_id: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    new_price: Optional[float] = 0.00


class ProductCreate(ProductBase):
    image_urls: List[str]


class Product(ProductBase):
    id: int
    image_urls: List[str]

    class Config:
        from_attributes = True
