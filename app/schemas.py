from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Create_Observation(BaseModel):

   Observation_Teacher: int 
   Observation_Class: str
   Observation_Focus: str
   Observation_Strengths: Optional[str]
   Observation_Weaknesses: Optional[str]
   Observation_Comments: Optional[str]

   class Config:
      orm_mode = True

class Observations_List(BaseModel):
   Observation_ID: int
   Observation_Date: datetime
   Teacher_Forename: Optional[str] = None
   Teacher_Surname: Optional[str] = None
   Observation_Class: str
   
   class Config:
      orm_mode = True

class Teachers_List(BaseModel):
   User_ID: int
   Teacher_Forename: str
   Teacher_Surname: str
   
   class Config:
      orm_mode = True