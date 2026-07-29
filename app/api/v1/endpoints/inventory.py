from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.inventory import InventoryResponse, InventoryCreate
from app.services.inventory_service import InventoryService

router = APIRouter()

@router.get("/", response_model=List[InventoryResponse])
def read_inventory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return InventoryService.get_all(db, skip=skip, limit=limit)

@router.get("/low-stock", response_model=List[InventoryResponse])
def read_low_stock_inventory(db: Session = Depends(get_db)):
    return InventoryService.get_low_stock(db)

@router.get("/{inventory_id}", response_model=InventoryResponse)
def read_inventory_item(inventory_id: int, db: Session = Depends(get_db)):
    inv = InventoryService.get_by_id(db, inventory_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return inv

@router.post("/", response_model=InventoryResponse, status_code=201)
def create_inventory_item(inventory_in: InventoryCreate, db: Session = Depends(get_db)):
    return InventoryService.create(db, inventory_in)
