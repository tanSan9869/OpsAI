from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class CustomerBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
