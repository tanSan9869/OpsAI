from datetime import datetime
from pydantic import BaseModel

class ProductBase(BaseModel):
    sku: str
    name: str
    category: str
    unit_price: float
    unit_cost: float

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
