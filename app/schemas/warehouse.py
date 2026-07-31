from datetime import datetime
from pydantic import BaseModel

class WarehouseBase(BaseModel):
    name: str
    location: str
    capacity: int = 10000

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseResponse(WarehouseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
