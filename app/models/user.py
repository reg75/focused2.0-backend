from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    # EN: Creates Users table
    # BR: Cria tabela 'Users' (Usuários)
    __tablename__ = "Users"
    User_ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    User_Forename = Column(String(64), nullable=False)
    User_Surname = Column(String(64), nullable=False)
    User_Email = Column(String(256), nullable=False, unique=True)
