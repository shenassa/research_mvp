from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.models import SubProject, Project, User
from datetime import date

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def require_user(request: Request, db: Session):
    user = get_current_user(request, db)

    if not user:
        return None

    return user


@router.get(
    "/projects/{project_id}/subprojects/new",
    response_class=HTMLResponse
)
def subproject_create_page(
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

    users = (
        db.query(User)
        .filter(User.is_active == True)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="subprojects/form.html",
        context={
            "user": user,
            "project": project,
            "subproject": None,
            "users": users
        }
    )


@router.post("/projects/{project_id}/subprojects/new")
def subproject_create(
    project_id: int,
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    manager_id: int = Form(None),
    status: str = Form("NOT_STARTED"),
    progress_percent: float = Form(0),
    start_date: str = Form(""),
    end_date: str = Form(""),
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

    start_date_obj = (
        date.fromisoformat(start_date)
        if start_date
        else None
    )

    end_date_obj = (
        date.fromisoformat(end_date)
        if end_date
        else None
    )

    subproject = SubProject(
        project_id=project_id,
        title=title,
        description=description,
        manager_id=manager_id,
        status=status,
        progress_percent=progress_percent,
        start_date=start_date_obj,
        end_date=end_date_obj
    )

    db.add(subproject)
    db.commit()

    return RedirectResponse(
        url=f"/projects/{project_id}",
        status_code=303
    )

@router.get(
    "/subprojects/{subproject_id}/edit",
    response_class=HTMLResponse
)
def subproject_edit_page(
    subproject_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    user = require_user(request, db)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    subproject = (
        db.query(SubProject)
        .filter(SubProject.id == subproject_id)
        .first()
    )

    if not subproject:
        return HTMLResponse(
            "زیرپروژه پیدا نشد.",
            status_code=404
        )

    users = (
        db.query(User)
        .filter(User.is_active == True)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="subprojects/form.html",
        context={
            "user": user,
            "project": subproject.project,
            "subproject": subproject,
            "users": users
        }
    )


@router.post("/subprojects/{subproject_id}/edit")
def subproject_edit(
    subproject_id: int,
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    manager_id: int = Form(None),
    status: str = Form("NOT_STARTED"),
    progress_percent: float = Form(0),
    start_date: str = Form(""),
    end_date: str = Form(""),
    db: Session = Depends(get_db)
):
    user = require_user(request, db)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    subproject = (
        db.query(SubProject)
        .filter(SubProject.id == subproject_id)
        .first()
    )

    if not subproject:
        return HTMLResponse(
            "زیرپروژه پیدا نشد.",
            status_code=404
        )

    start_date_obj = (
        date.fromisoformat(start_date)
        if start_date
        else None
    )

    end_date_obj = (
        date.fromisoformat(end_date)
        if end_date
        else None
    )

    subproject.title = title
    subproject.description = description
    subproject.manager_id = manager_id
    subproject.status = status
    subproject.progress_percent = progress_percent
    subproject.start_date = start_date_obj
    subproject.end_date = end_date_obj

    db.commit()

    return RedirectResponse(
        url=f"/projects/{subproject.project_id}",
        status_code=303
    )

@router.post("/subprojects/{subproject_id}/delete")
def subproject_delete(
    subproject_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    user = require_user(request, db)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    subproject = (
        db.query(SubProject)
        .filter(SubProject.id == subproject_id)
        .first()
    )

    if not subproject:
        return HTMLResponse(
            "زیرپروژه پیدا نشد.",
            status_code=404
        )

    project_id = subproject.project_id

    db.delete(subproject)
    db.commit()

    return RedirectResponse(
        url=f"/projects/{project_id}",
        status_code=303
    )