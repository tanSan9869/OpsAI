from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, index=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False, index=True)
    status = Column(String(30), nullable=False, index=True)  # pending, processing, shipped, delivered, delayed, cancelled
    total_amount = Column(Float, nullable=False, default=0.0)
    order_date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    expected_delivery = Column(DateTime, nullable=False)
    actual_delivery = Column(DateTime, nullable=True)

    customer = relationship("Customer", back_populates="orders")
    warehouse = relationship("Warehouse", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
