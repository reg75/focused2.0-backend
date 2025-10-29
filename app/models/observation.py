from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class FocusArea(Base):
    # EN: Creates FocusArea table
    # BR: Cria tabela 'Focus' (Foco)
    __tablename__ = "FocusAreas"
    FocusArea_ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    FocusArea_Name = Column(String(64), unique=True, nullable=False, index=True)

class Observation(Base):
    # EN: Creates Observations table
    # BR: Cria tabela 'Observations' (Observações de aula)
    __tablename__ = "Observations"
    Observation_ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Observation_Date = Column(DateTime, server_default=func.now(), nullable=False)
    Observation_Department = Column(Integer, ForeignKey("Departments.Department_ID"), index=True, nullable=False)
    department = relationship("Department", backref="observations")
    Observation_Teacher = Column(Integer, ForeignKey("Users.User_ID"), nullable=False, index=True)
    teacher = relationship("User", backref="observations") 
    Observation_Class = Column(String(16), nullable=False)
    Observation_Focus = Column(Integer, ForeignKey("FocusAreas.FocusArea_ID"), nullable=False, index=True)
    focus = relationship("FocusArea", backref="observations")
    Observation_Strengths = Column(String(1000))
    Observation_Weaknesses = Column(String(1000))
    Observation_Comments = Column(String(1000))
