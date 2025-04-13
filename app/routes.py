from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from weasyprint import HTML
from io import BytesIO
from typing import List
from sqlalchemy.orm import Session
from .models import Observation, User
from .database import get_db
from .schemas import Create_Observation, Observations_List, Teachers_List
import os

router = APIRouter()

@router.get("/observations", response_model=List[Observations_List])
def fetch_observations(db: Session = Depends(get_db)):
   # EN: Fetch all observations and join with Users to get teacher information
   # BR: Buscar todas as observações e juntar com os usuários para pegar as informações dos professores
   observations = db.query(Observation).join(User, Observation.Observation_Teacher == User.User_ID).all()

   # EN: Return a message if there are no observations
   # BR: Retorna uma mensagem se não houver observações
   if not observations: 
      return {"message": "No observations yet!"}

   # EN: Return the observations with teacher names
   # BR: Retorna as observações com os nomes dos professores
   return [
      Observations_List(
         Observation_ID=observation.Observation_ID,
         Observation_Date=observation.Observation_Date,
         Teacher_Forename=observation.teacher.User_Forename,
         Teacher_Surname=observation.teacher.User_Surname,
         Observation_Class=observation.Observation_Class,
         Observation_Focus=observation.Observation_Focus,
         Observation_Strengths=observation.Observation_Strengths,
         Observation_Weaknesses=observation.Observation_Weaknesses,
         Observation_Comments=observation.Observation_Comments,
    )
    for observation in observations
]


@router.post("/new")
def create_observation(observation: Create_Observation, db: Session = Depends(get_db)):
   # EN: Create a new observation
   # BR: Criar uma nova observação
   new_observation = Observation(**observation.dict())
   db.add(new_observation)
   db.commit()
   db.refresh(new_observation)
   return {"id": new_observation.Observation_ID}  

@router.get("/view/{observation_ID}")
def view_observation(observation_ID: int, db: Session = Depends(get_db)):
   # EN: View the details of an observation
   # BR: Visualizar os detalhes de uma observação
   observation = db.query(Observation).filter(Observation.Observation_ID == observation_ID).first()

   if not observation:
      raise HTTPException(status_code=404, detail="Observation not found")

   return {
      "Observation_ID": observation.Observation_ID,
      "Observation_Date": observation.Observation_Date,
      "Teacher_Forename": observation.teacher.User_Forename,
      "Teacher_Surname": observation.teacher.User_Surname,
      "Observation_Class": observation.Observation_Class,
      "Observation_Focus": observation.Observation_Focus,
      "Observation_Strengths": observation.Observation_Strengths,
      "Observation_Weaknesses": observation.Observation_Weaknesses,
      "Observation_Comments": observation.Observation_Comments,
   }


@router.delete("/observations/{observation_id}")
def delete_observation(observation_id: int, db: Session = Depends(get_db)):
   observation = db.query(Observation).filter(Observation.Observation_ID == observation_id).first()
   # EN: Delete an observation
   # BR: Apagar uma observação
   if observation is None:
      raise HTTPException(status_code=404, detail="Observation not found")
   db.delete(observation)
   db.commit()
   return {"message": "Observation deleted successfully"}


@router.get("/pdf/{id}")
async def create_pdf(id: int, db: Session = Depends(get_db)):
   # EN: download the PDF of an observation
   # BR: Baixar observação como arquivo PDF
   observation = db.query(Observation).filter(Observation.Observation_ID == id).first()
   if observation is None:
      raise HTTPException(status_code=404, detail="Observation not found")
    
   # EN: Generate HTML content for the PDF / Gerar contenudo HTML
   html_content = f"""
   <html>
      <head>
         <style>
               body {{ font-family: Arial, sans-serif; }}
               .title {{ font-size: 20px; }}
               .content {{ margin: 20px; }}
         </style>
      </head>
      <body>
         <h1 class="title">FocusEd Lesson Observation</h1>
         <div class="content">
               <p><strong>Teacher:</strong> {observation.Observation_Teacher}</p>+
               
               <p><strong>Date:</strong> {observation.Observation_Date}</p>
               <p><strong>Class:</strong> {observation.Observation_Class}</p>
               <p><strong>Focus Area:</strong> {observation.Observation_Focus}</p>
               <p><strong>Strengths:</strong> {observation.Observation_Strengths}</p>
               <p><strong>Areas for Development:</strong> {observation.Observation_Weaknesses}</p>
               <p><strong>Other Comments:</strong> {observation.Observation_Comments}</p>
         </div>
      </body>
   </html>
   """
    
   # Generate the PDF / Gerar arquivo pdf
   pdf = HTML(string=html_content).write_pdf()

   pdf_stream = BytesIO(pdf)
   pdf_stream.seek(0)

   # EN: Return the PDF as a downloadable file using StreamingResponse / BR: Retorna o PDF como um arquivo para download usando StreamingResponse
   return StreamingResponse(pdf_stream, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=observation_{id}.pdf"})

from fastapi import HTTPException

@router.get("/teachers", response_model=List[Teachers_List])
def fetch_teachers(db: Session = Depends(get_db)):
    # EN: Fetch all teachers from the database, ordered by surname
    # BR: Buscar todos os professores no banco de dados, ordenados por sobrenome
    teachers = db.query(User).order_by(User.User_Surname).all()

    # EN: Raise an error if no teachers are found
    # BR: Gerar um erro se nenhum professor for encontrado
    if not teachers:
        raise HTTPException(status_code=404, detail="No teachers found")

    # EN: Return a list of teachers
    # BR: Retornar uma lista de professores
    return [
        Teachers_List(
            User_ID=teacher.User_ID,
            Teacher_Forename=teacher.User_Forename,
            Teacher_Surname=teacher.User_Surname,
        )
        for teacher in teachers
    ]
