from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# EN: Not used in MVP / não usado no MVP
class FlagType(Base):
    # EN: Creates FlagTypes table
    # BR: Cria tabela 'FlagTypes' (tipos de indicador)
    __tablename__ = "FlagTypes"
    FlagType_ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    FlagType_Name = Column(String(64), unique=True, nullable=False)

# EN: Not used in MVP / não usado no MVP
class Flag(Base):
    # EN: Creates Flags table
    # BR: Cria tabela 'Flags' (indicadores)
    __tablename__ = "Flags"
    Flag_ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Observation = Column(Integer, ForeignKey("Observations.Observation_ID"), nullable=False, index=True)
    observation = relationship("Observation", backref="flags")
    FlagType = Column(Integer, ForeignKey("FlagTypes.FlagType_ID"), nullable=False, index=True)
    flag_type = relationship("FlagType", backref="flags")
    FocusArea = Column(Integer, ForeignKey("FocusAreas.FocusArea_ID"), nullable=False, index=True)
    focus = relationship("FocusArea", backref="flags")
    Is_Open = Column(Boolean, nullable=False, default=True)
