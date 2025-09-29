from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class ORMModel(BaseModel):
   model_config = ConfigDict(from_attributes=True)

# EN: Schema for creating new observation via API
# BR: Esquema para criar uma nova observação através da API
class Create_Observation(ORMModel):

   Observation_Teacher: int 
   Observation_Department: int
   Observation_Class: str
   Observation_Focus: int
   Observation_Strengths: Optional[str] = None
   Observation_Weaknesses: Optional[str] = None
   Observation_Comments: Optional[str] = None

# EN: Schema for updating an observation via API
# BR: Esquema para atualizar uma observação através da API
class Update_Observation(ORMModel):

   Observation_Teacher: int | None = None
   Observation_Department: int | None = None
   Observation_Class: str | None = None
   Observation_Focus: int  | None = None
   Observation_Strengths: str | None = None
   Observation_Weaknesses: str | None = None
   Observation_Comments: str | None = None

# EN: If true, backend will re-send the PDF email after saving
# BR: Se verdadeiro, backend reenviará o PDF por email após salvar
   resend_email: bool | None = False

# EN: Schema for creating list of observations via API  
# BR: Esquema para criar lista de observações via API
class Observations_List(ORMModel):
   Observation_ID: int
   Observation_Date: datetime
   Teacher_Forename: Optional[str] = None
   Teacher_Surname: Optional[str] = None
   Observation_Class: str
   Observation_Department: str
   Observation_Focus: str
   
# EN: Schema for returning list of departments  
# BR: Esquema para retornar uma lista de departamentos
class Departments_List(ORMModel):
   Department_ID: int
   Department_Name: str
   
# EN: Schema for returning list of teachers  
# BR: Esquema para retornar uma lista de professores
class Teachers_List(ORMModel):
   User_ID: int
   Teacher_Forename: str
   Teacher_Surname: str
   Teacher_Email: EmailStr
   
# EN: Schema for returning list of focus areas  
# BR: Esquema para retornar uma lista de focos
class FocusAreas_List(ORMModel):
   FocusArea_ID: int
   FocusArea_Name: str
   
# EN: Schema for returning list of flag types  
# BR: Esquema para retornar uma lista de tipos de indicador
class FlagTypes_List(ORMModel):
   FlagType_ID: int
   FlagType_Name: str

# EN: Schema for creating a new flag  
# BR: Esquema para criar um novo indicador
class Create_Flag(ORMModel):
   Observation: int
   FlagType: int
   FocusArea: int
   Is_Open: bool = True

class Flags_List(ORMModel):
   Flag_ID: int
   Teacher: str
   Focus_Area: str
   Flag_Date: datetime
   Is_Open: bool


