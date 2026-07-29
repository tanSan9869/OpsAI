from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.warehouse import WarehouseResponse, WarehouseCreate
from app.services.warehouse_service import WarehouseService

router = APIRouter()

@router.get("/", response_model=List[WarehouseResponse])
def read_warehouses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return WarehouseService.get_all(db, skip=skip, limit=limit)

@router.get("/{warehouse_id}", response_model=WarehouseResponse)
def read_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    wh = WarehouseService.get_by_id(db, warehouse_id)
    if not wh:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return wh

@router.post("/", response_model=WarehouseResponse, status_code=201)
def create_warehouse(warehouse_in: WarehouseCreate, db: Session = Depends(get_db)):
    return WarehouseService.create(db, warehouse_in)
