from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, DateTime
from datetime import datetime, timezone
from database.connection import Base
from sqlalchemy.orm import relationship
from models.order_model import OrderItem


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    new_price = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    images = relationship("ProductImage", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

    def __repr__(self):
        return f"Product: {self.name}"


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    image_url = Column(String)  # Store URL or path to image

    product = relationship("Product", back_populates="images")

    def __repr__(self):
        return f"ProductImage: {self.image_url} of {self.product.name}"
