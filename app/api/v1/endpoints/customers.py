from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.customer import CustomerResponse, CustomerCreate
from app.services.customer_service import CustomerService

router = APIRouter()

@router.get("/", response_model=List[CustomerResponse])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return CustomerService.get_all(db, skip=skip, limit=limit)

@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = CustomerService.get_by_id(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(customer_in: CustomerCreate, db: Session = Depends(get_db)):
    return CustomerService.create(db, customer_in)
