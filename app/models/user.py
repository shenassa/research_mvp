from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    full_name = Column(String(200), nullable=False)

    role = Column(String(50), nullable=False, default="DEPARTMENT_USER")
    is_active = Column(Boolean, default=True)

    department_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship("Department")