from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# EN: Schema for creating new observation via API
# BR: Esquema para criar uma nova observação através da API
class Create_Observation(BaseModel):

   Observation_Teacher: int 
   Observation_Class: str
   Observation_Focus: str
   Observation_Strengths: Optional[str]
   Observation_Weaknesses: Optional[str]
   Observation_Comments: Optional[str]

   class Config:
      orm_mode = True

# EN: Schema for creating list of observations via API  
# BR: Esquema para criar lista de observações via API
class Observations_List(BaseModel):
   Observation_ID: int
   Observation_Date: datetime
   Teacher_Forename: Optional[str] = None
   Teacher_Surname: Optional[str] = None
   Observation_Class: str
   
   class Config:
      orm_mode = True

# EN: Schema for returning list of teachers  
# BR: Esquema para retornar uma lista de professores
class Teachers_List(BaseModel):
   User_ID: int
   Teacher_Forename: str
   Teacher_Surname: str
   
   class Config:
      orm_mode = True