from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class ORMModel(BaseModel):
   model_config = ConfigDict(from_attributes=True)

# EN: Schema for creating new observation via API
# BR: Esquema para criar uma nova observação através da API
class Create_Observation(BaseModel):

   Observation_Teacher: int 
   Observation_Department: int
   Observation_Class: str
   Observation_Focus: int
   Observation_Strengths: Optional[str] = None
   Observation_Weaknesses: Optional[str] = None
   Observation_Comments: Optional[str] = None

# EN: Schema for creating list of observations via API  
# BR: Esquema para criar lista de observações via API
class Observations_List(BaseModel):
   Observation_ID: int
   Observation_Date: datetime
   Teacher_Forename: Optional[str] = None
   Teacher_Surname: Optional[str] = None
   Observation_Class: str
   Observation_Department: int
   Observation_Focus: int
   
# EN: Schema for returning list of departments  
# BR: Esquema para retornar uma lista de departamentos
class Departments_List(BaseModel):
   Department_ID: int
   Department_Name: str
   
# EN: Schema for returning list of teachers  
# BR: Esquema para retornar uma lista de professores
class Teachers_List(BaseModel):
   User_ID: int
   Teacher_Forename: str
   Teacher_Surname: str
   Teacher_Email: EmailStr
   
# EN: Schema for returning list of focus areas  
# BR: Esquema para retornar uma lista de focos
class FocusAreas_List(BaseModel):
   FocusArea_ID: int
   FocusArea_Name: str
   
# EN: Schema for returning list of flag types  
# BR: Esquema para retornar uma lista de tipos de indicador
class FlagTypes_List(BaseModel):
   FlagType_ID: int
   FlagType_Name: str
   