from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    role = Column(String(50), nullable=False, default="analyst")  # admin, analyst, manager
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
