from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    # EN: Creates Users table
    # BR: Cria tabela 'Users' (Usuários)
    __tablename__ = "Users"
    User_ID = Column(Integer, primary_key=True, index=True)
    User_Forename = Column(String(64), nullable=False)
    User_Surname = Column(String(64), nullable=False)
    User_Email = Column(String(128), nullable=False, unique=True)

class Observation(Base):
    # EN: Creates Observations table
    # BR: Cria tabela 'Observations' (Observações de aula)
    __tablename__ = "Observations"
    Observation_ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Observation_Date = Column(DateTime, default=func.now())
    Observation_Teacher = Column(Integer, ForeignKey("Users.User_ID"), nullable=False)
    teacher = relationship("User", backref="Observations") 
    Observation_Class = Column(String(8), nullable=False)
    Observation_Focus = Column(String(32), nullable=False)
    Observation_Strengths = Column(String(1000))
    Observation_Weaknesses = Column(String(1000))
    Observation_Comments = Column(String(1000))

# Creates initial list of users / teachers
# Cria lista inicial de usuários / professores
def create_initial_data(session):
    if session.query(User).count() == 0:
        users = [
            User(User_Forename="Chloe", User_Surname="Chen", User_Email="chloe@myschool.co.uk"),
            User(User_Forename="Colleen", User_Surname="Murphy", User_Email="colleen@myschool.co.uk"),
            User(User_Forename="Peter", User_Surname="Robinson", User_Email="peter@myschool.co.uk"),
            User(User_Forename="Laura", User_Surname="Williams", User_Email="laura@myschool.co.uk"),
        ]
        session.add_all(users)
        session.commit()
