from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database.base import Base

class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False, default=10000)
    created_at = Column(DateTime, default=datetime.utcnow)

    inventory_items = relationship("Inventory", back_populates="warehouse")
    orders = relationship("Order", back_populates="warehouse")
