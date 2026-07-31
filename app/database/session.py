import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

logger = logging.getLogger(__name__)

db_url = settings.sync_database_url

def create_db_engine():
    global db_url
    try:
        if settings.USE_SQLITE_FALLBACK and "postgresql" in db_url:
            # Test PostgreSQL connection attempt or fallback directly if requested
            engine = create_engine(db_url, pool_pre_ping=True, connect_args={"connect_timeout": 2})
            with engine.connect() as conn:
                pass
            logger.info("Successfully connected to PostgreSQL database.")
            return engine
        elif "sqlite" in db_url:
            return create_engine(db_url, connect_args={"check_same_thread": False})
        else:
            return create_engine(db_url, pool_pre_ping=True)
    except Exception as e:
        logger.warning(f"Could not connect to PostgreSQL ({e}). Falling back to SQLite database.")
        db_url = "sqlite:///./opsai.db"
        return create_engine(db_url, connect_args={"check_same_thread": False})

engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
