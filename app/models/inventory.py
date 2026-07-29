from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.base import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    stock_quantity = Column(Integer, nullable=False, default=0)
    reorder_level = Column(Integer, nullable=False, default=10)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    warehouse = relationship("Warehouse", back_populates="inventory_items")
    product = relationship("Product", back_populates="inventory_items")
