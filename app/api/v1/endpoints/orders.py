from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.order import OrderResponse, OrderCreate
from app.services.order_service import OrderService

router = APIRouter()

@router.get("/", response_model=List[OrderResponse])
def read_orders(
    status: Optional[str] = Query(None, description="Filter orders by status (e.g., delayed, pending, delivered)"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return OrderService.get_all(db, status=status, skip=skip, limit=limit)

@router.get("/delayed", response_model=List[OrderResponse])
def read_delayed_orders(db: Session = Depends(get_db)):
    return OrderService.get_delayed(db)

@router.get("/{order_id}", response_model=OrderResponse)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = OrderService.get_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    return OrderService.create(db, order_in)
