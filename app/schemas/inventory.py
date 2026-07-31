from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.product import ProductResponse
from app.schemas.warehouse import WarehouseResponse

class InventoryBase(BaseModel):
    warehouse_id: int
    product_id: int
    stock_quantity: int
    reorder_level: int = 10

class InventoryCreate(InventoryBase):
    pass

class InventoryResponse(InventoryBase):
    id: int
    last_updated: datetime
    product: Optional[ProductResponse] = None
    warehouse: Optional[WarehouseResponse] = None

    class Config:
        from_attributes = True
