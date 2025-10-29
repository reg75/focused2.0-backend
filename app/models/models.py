from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

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
            User(User_Forename="Chloe", User_Surname="Chen", User_Email="focused-app.user1@maildrop.cc"),
            User(User_Forename="Colleen", User_Surname="Murphy", User_Email="focused-app.user2@maildrop.cc"),
            User(User_Forename="Peter", User_Surname="Robinson", User_Email="focused-app.user3@maildrop.cc"),
            User(User_Forename="Laura", User_Surname="Williams", User_Email="focused-app.user4@maildrop.cc"),
            User(User_Forename="Steven", User_Surname="Ingram", User_Email="focused-app.user5@maildrop.cc"),
            User(User_Forename="Anna", User_Surname="Masters", User_Email="focused-app.user6@maildrop.cc"),
            User(User_Forename="Taissa", User_Surname="Hubbard", User_Email="focused-app.user7@maildrop.cc"),
            User(User_Forename="Sally", User_Surname="Mannon", User_Email="focused-app.user8@maildrop.cc"),
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

        

        
