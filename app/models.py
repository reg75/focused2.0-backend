from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Department(Base):
    # EN: Creates Departments table
    # BR: Cria table 'Departments' (Departamentos)
    __tablename__ = "Departments"
    Department_ID = Column(Integer, primary_key=True, autoincrement=True)
    Department_Name = Column(String(128), unique=True, nullable=False)

class User(Base):
    # EN: Creates Users table
    # BR: Cria tabela 'Users' (Usuários)
    __tablename__ = "Users"
    User_ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    User_Forename = Column(String(64), nullable=False)
    User_Surname = Column(String(64), nullable=False)
    User_Email = Column(String(256), nullable=False, unique=True)

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

class FlagType(Base):
    # EN: Creates FlagTypes table
    # BR: Cria tabela 'FlagTypes' (tipos de indicador)
    __tablename__ = "FlagTypes"
    FlagType_ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    FlagType_Name = Column(String(64), unique=True, nullable=False)

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
    Is_Active = Column(Boolean, nullable=False, default=True)

# Creates initial list of users / teachers
# Cria lista inicial de usuários / professores
def create_initial_data(session):
    if session.query(Department).count() == 0:
        departments = [
            Department(Department_Name="Religious Studies"),
            Department(Department_Name="Computing"),
            Department(Department_Name="French"),
            
        ]
    
        session.add_all(departments)
        session.commit()


    if session.query(User).count() == 0:
        users = [
            User(User_Forename="Chloe", User_Surname="Chen", User_Email="chloe@myschool.co.uk"),
            User(User_Forename="Colleen", User_Surname="Murphy", User_Email="colleen@myschool.co.uk"),
            User(User_Forename="Peter", User_Surname="Robinson", User_Email="peter@myschool.co.uk"),
            User(User_Forename="Laura", User_Surname="Williams", User_Email="laura@myschool.co.uk"),
            User(User_Forename="Steven", User_Surname="Ingram", User_Email="steven@myschool.co.uk"),
            User(User_Forename="Anna", User_Surname="Masters", User_Email="anna@myschool.co.uk"),
            User(User_Forename="Taissa", User_Surname="Hubbard", User_Email="taissa@myschool.co.uk"),
            User(User_Forename="Sally", User_Surname="Mannon", User_Email="sally@myschool.co.uk"),
        ]
    
        session.add_all(users)
        session.commit()

    if session.query(FocusArea).count() == 0:
        focus_areas = [
            FocusArea(FocusArea_Name="Synoptic"),
            FocusArea(FocusArea_Name="Subject knowledge"),
            FocusArea(FocusArea_Name="Explanations"),
            FocusArea(FocusArea_Name="Questioning"),
            FocusArea(FocusArea_Name="Feedback"),
            FocusArea(FocusArea_Name="Modelling"),
            FocusArea(FocusArea_Name="Metacognition"),
            FocusArea(FocusArea_Name="Memory"),
            FocusArea(FocusArea_Name="Behaviour"),
        ]

        session.add_all(focus_areas)
        session.commit()

    if session.query(FlagType).count() == 0:
        flag_types = [
            FlagType(FlagType_Name="Exemplary"),
            FlagType(FlagType_Name="Practice Alert"),
        ]

        session.add_all(flag_types)
        session.commit()

        

        
