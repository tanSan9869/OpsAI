from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.schemas.customer import CustomerResponse
from app.schemas.warehouse import WarehouseResponse
from app.schemas.product import ProductResponse

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    product: Optional[ProductResponse] = None

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    order_number: str
    customer_id: int
    warehouse_id: int
    status: str
    total_amount: float
    order_date: datetime
    expected_delivery: datetime
    actual_delivery: Optional[datetime] = None

class OrderCreate(OrderBase):
    items: List[OrderItemCreate] = []

class OrderResponse(OrderBase):
    id: int
    customer: Optional[CustomerResponse] = None
    warehouse: Optional[WarehouseResponse] = None
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True
