from fastapi import APIRouter
from app.api.v1.endpoints import health, auth, customers, products, warehouses, inventory, orders, chat

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(customers.router, prefix="/customers", tags=["Customers"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(warehouses.router, prefix="/warehouses", tags=["Warehouses"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])
api_router.include_router(chat.router, prefix="/chat", tags=["AI Chat & NL2SQL Agent"])
