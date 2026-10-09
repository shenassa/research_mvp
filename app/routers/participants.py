from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.models import Project, ProjectParticipant


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def require_user(request: Request, db: Session):
    user = get_current_user(request, db)

    if not user:
        return None

    return user


@router.get(
    "/projects/{project_id}/participants/new",
    response_class=HTMLResponse
)
def participant_create_page(
    project_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    user = require_user(request, db)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        return HTMLResponse(
            "پروژه پیدا نشد.",
            status_code=404
        )

    return templates.TemplateResponse(
        request=request,
        name="participants/form.html",
        context={
            "user": user,
            "project": project
        }
    )


@router.post("/projects/{project_id}/participants/new")
def participant_create(
    project_id: int,
    request: Request,
    name: str = Form(...),
    organization: str = Form(""),
    role: str = Form(""),
    db: Session = Depends(get_db)
):
    user = require_user(request, db)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        return HTMLResponse(
            "پروژه پیدا نشد.",
            status_code=404
        )

    participant = ProjectParticipant(
        project_id=project_id,
        name=name,
        organization=organization,
        role=role
    )

    db.add(participant)
    db.commit()

    return RedirectResponse(
        url=f"/projects/{project_id}",
        status_code=303
    )


@router.post("/participants/{participant_id}/delete")
def participant_delete(
    participant_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    user = require_user(request, db)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    participant = (
        db.query(ProjectParticipant)
        .filter(ProjectParticipant.id == participant_id)
        .first()
    )

    if not participant:
        return HTMLResponse(
            "مشارکت‌کننده پیدا نشد.",
            status_code=404
        )

    project_id = participant.project_id

    db.delete(participant)
    db.commit()

    return RedirectResponse(
        url=f"/projects/{project_id}",
        status_code=303
    )