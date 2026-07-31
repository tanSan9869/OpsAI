import logging
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from app.database.session import engine, SessionLocal
from app.database.base import Base
import app.models  # Register models
from app.models import Customer, Product, Warehouse, Inventory, Order, OrderItem, User
from app.core.security import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")

def seed_database():
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    try:
        # Check if users already exist
        if not db.query(User).filter(User.email == "admin@opsai.com").first():
            logger.info("Seeding initial user accounts...")
            admin_user = User(
                email="admin@opsai.com",
                hashed_password=get_password_hash("admin123"),
                full_name="OpsAI Admin",
                role="admin",
                is_active=True
            )
            analyst_user = User(
                email="analyst@opsai.com",
                hashed_password=get_password_hash("analyst123"),
                full_name="Operations Analyst",
                role="analyst",
                is_active=True
            )
            db.add_all([admin_user, analyst_user])
            db.commit()

        # Check if operational data already exists
        if db.query(Customer).first():
            logger.info("Database operational data already seeded. Skipping operational seed.")
            return

        logger.info("Seeding operational data...")

        # 1. Seed Warehouses
        warehouses = [
            Warehouse(name="North Distribution Center", location="Chicago, IL", capacity=15000),
            Warehouse(name="West Coast Hub", location="Los Angeles, CA", capacity=25000),
            Warehouse(name="East Coast Depot", location="Newark, NJ", capacity=20000),
            Warehouse(name="Central Fulfillment Center", location="Dallas, TX", capacity=18000),
        ]
        db.add_all(warehouses)
        db.flush()

        # 2. Seed Customers
        customers = [
            Customer(name="Apex Logistics Group", email="procurement@apexlogistics.com", phone="+1-555-0192", city="Chicago", region="Midwest"),
            Customer(name="Summit Tech Solutions", email="supply@summittech.io", phone="+1-555-0283", city="San Francisco", region="West"),
            Customer(name="Vanguard Retailers", email="orders@vanguardretail.com", phone="+1-555-0374", city="New York", region="East"),
            Customer(name="Horizon Enterprises", email="buying@horizonent.com", phone="+1-555-0465", city="Austin", region="South"),
            Customer(name="Pinnacle Industrial Parts", email="ops@pinnacleparts.com", phone="+1-555-0556", city="Detroit", region="Midwest"),
            Customer(name="Atlas Global Supply", email="contact@atlasglobal.com", phone="+1-555-0647", city="Seattle", region="West"),
            Customer(name="Brite Horizon Goods", email="purchasing@britehorizon.com", phone="+1-555-0738", city="Miami", region="South"),
            Customer(name="Crestview Merchants", email="inventory@crestview.com", phone="+1-555-0829", city="Boston", region="East"),
        ]
        db.add_all(customers)
        db.flush()

        # 3. Seed Products
        products = [
            Product(sku="PRD-ELEC-001", name="Industrial IoT Sensor Hub", category="Electronics", unit_price=249.99, unit_cost=140.00),
            Product(sku="PRD-ELEC-002", name="Smart Warehouse Scanner Pro", category="Electronics", unit_price=499.50, unit_cost=290.00),
            Product(sku="PRD-MACH-001", name="Automated Conveyor Motor 500W", category="Machinery", unit_price=850.00, unit_cost=510.00),
            Product(sku="PRD-MACH-002", name="Pneumatic Valve Assembly", category="Machinery", unit_price=120.00, unit_cost=65.00),
            Product(sku="PRD-PACK-001", name="Heavy Duty Pallet Wrapper", category="Packaging", unit_price=1200.00, unit_cost=750.00),
            Product(sku="PRD-PACK-002", name="Reinforced Shipping Container (Set of 10)", category="Packaging", unit_price=85.00, unit_cost=45.00),
            Product(sku="PRD-SAFE-001", name="High-Vis Safety Helmet & Gear Set", category="Safety", unit_price=65.00, unit_cost=30.00),
            Product(sku="PRD-SAFE-002", name="Thermal Barrier Work Gloves (Pair)", category="Safety", unit_price=24.99, unit_cost=10.00),
        ]
        db.add_all(products)
        db.flush()

        # 4. Seed Inventory across Warehouses
        inventory_items = []
        for wh in warehouses:
            for prd in products:
                stock = random.choice([3, 5, 8, 45, 120, 300])
                inventory_items.append(
                    Inventory(
                        warehouse_id=wh.id,
                        product_id=prd.id,
                        stock_quantity=stock,
                        reorder_level=15
                    )
                )
        db.add_all(inventory_items)
        db.flush()

        # 5. Seed Orders (with explicit delayed orders for test cases)
        now = datetime.utcnow()
        statuses = ["delivered", "shipped", "pending", "delayed", "delayed", "delivered", "delayed"]
        
        orders = []
        order_idx = 1001

        for i in range(16):
            cust = customers[i % len(customers)]
            wh = warehouses[i % len(warehouses)]
            status = statuses[i % len(statuses)]
            
            order_date = now - timedelta(days=random.randint(1, 20))
            expected_delivery = order_date + timedelta(days=4)
            
            actual_delivery = None
            if status == "delivered":
                actual_delivery = expected_delivery - timedelta(hours=random.randint(1, 12))
            elif status == "delayed":
                expected_delivery = now - timedelta(days=random.randint(1, 5))

            order = Order(
                order_number=f"ORD-2026-{order_idx}",
                customer_id=cust.id,
                warehouse_id=wh.id,
                status=status,
                total_amount=0.0,
                order_date=order_date,
                expected_delivery=expected_delivery,
                actual_delivery=actual_delivery
            )
            orders.append(order)
            order_idx += 1

        db.add_all(orders)
        db.flush()

        # 6. Seed Order Items
        for ord_obj in orders:
            selected_products = random.sample(products, k=random.randint(1, 3))
            total = 0.0
            for prd in selected_products:
                qty = random.randint(1, 10)
                item_price = prd.unit_price
                total += item_price * qty
                
                item = OrderItem(
                    order_id=ord_obj.id,
                    product_id=prd.id,
                    quantity=qty,
                    unit_price=item_price
                )
                db.add(item)
            
            ord_obj.total_amount = round(total, 2)

        db.commit()
        logger.info("Database successfully seeded with users and operational data!")

    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
