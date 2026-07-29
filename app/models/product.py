from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from app.database.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(150), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    unit_price = Column(Float, nullable=False)
    unit_cost = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    inventory_items = relationship("Inventory", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
