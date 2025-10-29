from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Department(Base):
    # EN: Creates Departments table
    # BR: Cria table 'Departments' (Departamentos)
    __tablename__ = "Departments"
    Department_ID = Column(Integer, primary_key=True, autoincrement=True)
    Department_Name = Column(String(128), unique=True, nullable=False)
