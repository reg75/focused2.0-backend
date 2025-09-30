# EN: Load .env early once / BR: Carregar .env cedo e uma única vez
import os
import httpx

from io import BytesIO
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks, Request, status, Response
from fastapi.responses import StreamingResponse
from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload

from .models import Observation, User, Department, FocusArea
from .database import get_db
from .schemas import (
    Create_Observation,
    Observations_List,
    Teachers_List,
    Update_Observation,
    Departments_List,
    FocusAreas_List,
)
from .mailer_client import notify_observation

router = APIRouter()
RENDERER_URL = os.getenv("RENDERER_URL", "http://renderer:8002")


# EN: ---- Helpers (internal) ---- / BR: ---- Auxiliares (internos) ----
def _build_mail_payload(request: Request, obs: Observation, teacher: Optional[User], dept: Optional[Department], focus: Optional[FocusArea]) -> dict:
    """EN: Create a consistent payload for the mailer / BR: Criar payload consistente para o mailer"""
    # EN: Teacher bits / BR: Dados do professor
    teacher_email = getattr(teacher, "User_Email", None) if teacher else None
    teacher_name = (
        f"{getattr(teacher, 'User_Forename', '')} {getattr(teacher, 'User_Surname', '')}".strip()
        if teacher else "Teacher"
    )

    # EN: Department/Focus names / BR: Nomes de Departamento/Foco
    dept_name = getattr(dept, "Department_Name", None) if dept else None
    focus_area_name = getattr(focus, "FocusArea_Name", None) if focus else None

    # EN: Date string / BR: Data como string
    try:
        obs_date_str = obs.Observation_Date.date().isoformat()
    except Exception:
        obs_date_str = str(obs.Observation_Date)

    # EN: Build absolute PDF URL / BR: Construir URL absoluto do PDF
    base = str(request.base_url).rstrip("/")
    pdf_url = f"{base}/api/pdf/{obs.Observation_ID}"

    return {
        "observation_id": obs.Observation_ID,
        "to_email": teacher_email,                # EN: align with mailer / BR: alinhar com o mailer
        "teacher_name": teacher_name,
        "obs_date": obs_date_str,
        "department_name": dept_name,
        "class_name": obs.Observation_Class or None,
        "focus_area": focus_area_name,
        "strengths": obs.Observation_Strengths or None,
        "weaknesses": getattr(obs, "Observation_Weaknesses", None),
        "comments": obs.Observation_Comments or None,
        "pdf_url": pdf_url,
    }


def _queue_email(bg: Optional[BackgroundTasks], payload: dict) -> None:
    """EN: Queue mailer via BackgroundTasks or run sync as fallback / BR: Enfileirar mailer via BackgroundTasks ou executar síncrono"""
    if bg is not None:
        bg.add_task(notify_observation, payload)
    else:
        # EN: Fallback (blocking) / BR: Alternativa (bloqueante)
        notify_observation(payload)


# EN: ---- Observations: list with optional filters ---- / BR: ---- Observações: listar com filtros opcionais ----
@router.get("/observations", response_model=List[Observations_List])
def fetch_observations(
    teacher_id: Optional[int] = Query(None, ge=1),
    department_id: Optional[int] = Query(None, ge=1),
    focus_area_id: Optional[int] = Query(None, ge=1),
    db: Session = Depends(get_db),
):
    # EN: Base query with joins / BR: Consulta base com joins
    q = (
        db.query(Observation)
        .options(
            joinedload(Observation.teacher),
            joinedload(Observation.department),
            joinedload(Observation.focus),
        )
    )

    # EN: Allows observations to be filtered / BR: Permite filtrar as observações
    filters = []
    if teacher_id is not None:
        filters.append(Observation.Observation_Teacher == teacher_id)
    if department_id is not None:
        filters.append(Observation.Observation_Department == department_id)
    if focus_area_id is not None:
        filters.append(Observation.Observation_Focus == focus_area_id)
    if filters:
        q = q.filter(*filters)

    observations = q.order_by(desc(Observation.Observation_Date)).all()

    # EN: Return empty list if none / BR: Retorna lista vazia se não houver
    if not observations:
        return []

    # EN: Map to response schema (defensive) / BR: Mapear para o schema de resposta (defensivo)
    out: List[Observations_List] = []
    for ob in observations:
        teacher = getattr(ob, "teacher", None)
        dept = getattr(ob, "department", None)
        foc = getattr(ob, "focus", None)
        out.append(
            Observations_List(
                Observation_ID=ob.Observation_ID,
                Observation_Date=ob.Observation_Date,
                Teacher_Forename=getattr(teacher, "User_Forename", None),
                Teacher_Surname=getattr(teacher, "User_Surname", None),
                Observation_Class=ob.Observation_Class,
                Observation_Department=getattr(dept, "Department_Name", None),
                Observation_Focus=getattr(foc, "FocusArea_Name", None),
            )
        )
    return out


# EN: ---- Create observation (optionally send) ---- / BR: ---- Criar observação (opcionalmente enviar) ----
@router.post("/new")
def create_observation(
    observation: Create_Observation,
    notify: bool = Query(False, description="If true, queue an email to teacher"),
    bg: BackgroundTasks = None,  # EN: injected by FastAPI / BR: injetado pelo FastAPI
    request: Request = None,
    db: Session = Depends(get_db),
):
    # EN: Create + persist / BR: Criar + persistir
    new_observation = Observation(**observation.model_dump())
    db.add(new_observation)
    db.commit()
    db.refresh(new_observation)

    print(f"[POST /new] notify={notify} new_id={new_observation.Observation_ID}")
    print(f"[POST /new] bg is None? {bg is None}")

    if notify:
        # EN: Load relations for payload / BR: Carregar relações para o payload
        teacher = db.query(User).filter(User.User_ID == new_observation.Observation_Teacher).first()
        dept = None
        if getattr(new_observation, "Observation_Department", None) is not None:
            dept = db.query(Department).filter(Department.Department_ID == new_observation.Observation_Department).first()
        focus = None
        if getattr(new_observation, "Observation_Focus", None) is not None:
            focus = db.query(FocusArea).filter(FocusArea.FocusArea_ID == new_observation.Observation_Focus).first()

        payload = _build_mail_payload(request, new_observation, teacher, dept, focus)
        print("[POST /new] queuing mailer task with payload:", payload)
        try:
            _queue_email(bg, payload)
        except Exception as e:
            # EN: Surface mailer failure separately / BR: Tratar falha do mailer separadamente
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Mailer call failed: {e}")

    # EN: Return the new ID (frontend needs this) / BR: Retornar o novo ID (frontend precisa)
    return {"id": new_observation.Observation_ID}


# EN: ---- Dedicated email trigger (fixes 404) ---- / BR: ---- Disparo dedicado de e-mail (corrige 404) ----
@router.post("/observations/{observation_id}/email")
def send_observation_email(
    observation_id: int,
    notify: bool = Query(False, description="Optional flag for logging only"),
    bg: BackgroundTasks = None,
    request: Request = None,
    db: Session = Depends(get_db),
):
    # EN: Load observation + relations / BR: Carregar observação + relações
    obs = (
        db.query(Observation)
        .options(
            joinedload(Observation.teacher),
            joinedload(Observation.department),
            joinedload(Observation.focus),
        )
        .filter(Observation.Observation_ID == observation_id)
        .first()
    )
    if not obs:
        raise HTTPException(status_code=404, detail="Observation not found")

    teacher = getattr(obs, "teacher", None)
    dept = getattr(obs, "department", None)
    focus = getattr(obs, "focus", None)

    payload = _build_mail_payload(request, obs, teacher, dept, focus)

    try:
        _queue_email(bg, payload)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Mailer call failed: {e}")

    return {"message": "Email queued"}


# EN: View a single observation / BR: Visualizar uma observação
@router.get("/observations/{observation_ID}")
def view_observation(observation_ID: int, db: Session = Depends(get_db)):
    obs = (
        db.query(Observation)
        .options(
            joinedload(Observation.teacher),
            joinedload(Observation.department),
            joinedload(Observation.focus),
        )
        .filter(Observation.Observation_ID == observation_ID)
        .first()
    )
    if not obs:
        raise HTTPException(status_code=404, detail="Observation not found")

    t = getattr(obs, "teacher", None)
    d = getattr(obs, "department", None)
    f = getattr(obs, "focus", None)

    return {
        "Observation_ID": obs.Observation_ID,
        "Observation_Date": obs.Observation_Date.isoformat() if obs.Observation_Date else None,
        "Observation_Class": obs.Observation_Class,
        "Observation_Strengths": obs.Observation_Strengths,
        "Observation_Weaknesses": obs.Observation_Weaknesses,
        "Observation_Comments": obs.Observation_Comments,

        # ✅ IDs (what the edit form must POST/PUT back)
        "Observation_Teacher": getattr(t, "User_ID", None),
        "Observation_Department": getattr(d, "Department_ID", None),
        "Observation_Focus": getattr(f, "FocusArea_ID", None),

        # ✅ Friendly names (nice for UI display)
        "Teacher_Forename": getattr(t, "User_Forename", None),
        "Teacher_Surname": getattr(t, "User_Surname", None),
        "Teacher_FullName": (
            f"{getattr(t,'User_Forename','')} {getattr(t,'User_Surname','')}".strip() if t else None
        ),
        "Department_Name": getattr(d, "Department_Name", None),
        "Focus_Name": getattr(f, "FocusArea_Name", None),
    }


# EN: Edit observation (with optional re-send) / BR: Editar observação (com reenvio opcional)
@router.put("/observations/{observation_ID}")
def edit_observation(
    observation_ID: int,
    changes: Update_Observation,
    bg: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    observation = (
        db.query(Observation)
        .options(
            joinedload(Observation.teacher),
            joinedload(Observation.department),
            joinedload(Observation.focus),
        )
        .filter(Observation.Observation_ID == observation_ID)
        .first()
    )
    if not observation:
        raise HTTPException(status_code=404, detail="Observation not found.")

    # EN: If user only wants to re-send, allow it (no 400) / BR: Permitir reenvio sem mudanças
    nothing_to_update = all(
        getattr(changes, field) is None
        for field in [
            "Observation_Teacher",
            "Observation_Department",
            "Observation_Class",
            "Observation_Focus",
            "Observation_Strengths",
            "Observation_Weaknesses",
            "Observation_Comments",
        ]
    )
    if nothing_to_update and not changes.resend_email:
        raise HTTPException(status_code=400, detail="Nothing to update")

    # EN: Dict of provided fields only / BR: Apenas campos enviados
    update_data = changes.model_dump(exclude_unset=True)
    update_data.pop("resend_email", None)

    # EN: Foreign keys first / BR: Chaves estrangeiras primeiro
    if "Observation_Teacher" in update_data:
        observation.Observation_Teacher = update_data["Observation_Teacher"]
    if "Observation_Department" in update_data:
        observation.Observation_Department = update_data["Observation_Department"]
    if "Observation_Focus" in update_data:
        observation.Observation_Focus = update_data["Observation_Focus"]

    # EN: Scalars / BR: Campos simples
    for field in ["Observation_Class", "Observation_Strengths", "Observation_Weaknesses", "Observation_Comments"]:
        if field in update_data:
            setattr(observation, field, update_data[field])

    db.commit()

    # EN: If re-sending, ensure relationships reflect any FK changes / BR: Recarregar relações
    if changes.resend_email:
        # simplest: re-query with joinedload so teacher/department/focus are fresh
        observation = (
            db.query(Observation)
            .options(
                joinedload(Observation.teacher),
                joinedload(Observation.department),
                joinedload(Observation.focus),
            )
            .filter(Observation.Observation_ID == observation_ID)
            .first()
        )

        teacher = getattr(observation, "teacher", None)
        dept = getattr(observation, "department", None)
        focus = getattr(observation, "focus", None)
        payload = _build_mail_payload(request, observation, teacher, dept, focus)
        _queue_email(bg, payload)

    return {"message": "Observation updated", "Observation_ID": observation.Observation_ID}

# EN: Delete observation / BR: Apagar observação
@router.delete("/observations/{observation_id}")
def delete_observation(observation_id: int, db: Session = Depends(get_db)):
    observation = db.query(Observation).filter(Observation.Observation_ID == observation_id).first()
    # EN: Delete an observation / BR: Apagar uma observação
    if observation is None:
        raise HTTPException(status_code=404, detail="Observation not found")
    db.delete(observation)
    db.commit()
    return {"message": "Observation deleted successfully"}


# EN: Generate PDF via renderer / BR: Gerar PDF via renderer
@router.get("/pdf/{id}")
async def create_pdf(id: int, db: Session = Depends(get_db)):
    observation = (
        db.query(Observation)
        .options(joinedload(Observation.teacher), joinedload(Observation.focus))
        .filter(Observation.Observation_ID == id)
        .first()
    )
    if observation is None:
        raise HTTPException(status_code=404, detail="Observation not found")

    teacher = getattr(observation, "teacher", None)
    focus   = getattr(observation, "focus", None)

    teacher_full_name = f"{getattr(teacher, 'User_Forename', '')} {getattr(teacher, 'User_Surname', '')}".strip()
    focus_label = (
        getattr(focus, "FocusArea_Name", None)
        or str(getattr(observation, "Observation_Focus", "—"))
    )
    date_str = str(getattr(observation, "Observation_Date", "—"))

    html_content = f"""
    <!doctype html><meta charset="utf-8">
    <style>
      body {{ font-family: DejaVu Sans, Arial, sans-serif; margin: 2rem; }}
      h1 {{ font-size: 22px; border-bottom: 1px solid #ccc; padding-bottom: .4rem; }}
      .content p {{ margin: .4rem 0; }}
      .label {{ font-weight: bold; }}
    </style>
    <h1>FocusEd Lesson Observation</h1>
    <div class="content">
      <p><span class="label">Teacher:</span> {teacher_full_name or '—'}</p>
      <p><span class="label">Date:</span> {date_str}</p>
      <p><span class="label">Class:</span> {observation.Observation_Class or '—'}</p>
      <p><span class="label">Focus Area:</span> {focus_label}</p>
      <p><span class="label">Strengths:</span> {observation.Observation_Strengths or '—'}</p>
      <p><span class="label">Areas for Development:</span> {observation.Observation_Weaknesses or '—'}</p>
      <p><span class="label">Other Comments:</span> {observation.Observation_Comments or '—'}</p>
    </div>
    """

    # Calls renderer / Chama renderer
    render_endpoint = f"{RENDERER_URL}/render"
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(render_endpoint, json={"html": html_content})
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Renderer unreachable: {e}") from e

    if r.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Renderer error (status {r.status_code})")

    ctype = r.headers.get("content-type", "").lower()
    if "application/pdf" not in ctype:
        raise HTTPException(status_code=502, detail=f"Renderer returned non-PDF (content-type {ctype})")

    filename = f"observation_{id}.pdf"
    headers = {"Content-Disposition": f'inline; filename="{filename}"'}
    return Response(content=r.content, media_type="application/pdf", headers=headers)


# EN Teachers / BR: Professores
@router.get("/teachers", response_model=List[Teachers_List])
def fetch_teachers(db: Session = Depends(get_db)):
    # EN: Fetch all teachers from the database, ordered by surname
    # BR: Buscar todos os professores no banco de dados, ordenados por sobrenome
    teachers = db.query(User).order_by(User.User_Surname).all()

    # EN: Raise error if no teachers are found / BR: Gerar erro se nenhum professor for encontrado
    if not teachers:
        raise HTTPException(status_code=404, detail="No teachers found")

    # EN: Return list of teachers / BR: Retornar lista de professores
    return [
        Teachers_List(
            User_ID=teacher.User_ID,
            Teacher_Forename=teacher.User_Forename,
            Teacher_Surname=teacher.User_Surname,
            Teacher_Email=teacher.User_Email,
        )
        for teacher in teachers
    ]


# EN: ---- Departments ---- / BR: ---- Departamentos ----
@router.get("/departments", response_model=List[Departments_List])
def fetch_departments(db: Session = Depends(get_db)):
    # EN: Fetch all departments from the database, ordered by name
    # BR: Buscar todos os departamentos no banco de dados, ordenados por nome
    departments = db.query(Department).order_by(Department.Department_Name).all()

    # EN: Raise error if no departments are found / BR: Gerar erro se nenhum departamento for encontrado
    if not departments:
        raise HTTPException(status_code=404, detail="No departments found")

    # EN: Return list of departments / BR: Retornar lista de departamentos
    return [
        Departments_List(
            Department_ID=department.Department_ID,
            Department_Name=department.Department_Name,
        )
        for department in departments
    ]


# EN: ---- Focus Areas ---- / BR: ---- Áreas de Foco ----
@router.get("/focus_areas", response_model=List[FocusAreas_List])
def fetch_focus_areas(db: Session = Depends(get_db)):
    # EN: Fetch all focus areas from the database, ordered by name
    # BR: Buscar todas as áreas de foco no banco de dados, ordenados por nome
    focus_areas = db.query(FocusArea).order_by(FocusArea.FocusArea_Name).all()

    # EN: Raise error if no focus areas are found / BR: Gerar erro se nenhuma área de foco for encontrada
    if not focus_areas:
        raise HTTPException(status_code=404, detail="No focus areas found")

    # EN: Return list of focus areas / BR: Retornar lista de áreas de foco
    return [
        FocusAreas_List(
            FocusArea_ID=focus_area.FocusArea_ID,
            FocusArea_Name=focus_area.FocusArea_Name,
        )
        for focus_area in focus_areas
    ]
