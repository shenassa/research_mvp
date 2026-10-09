from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.models import Project, User, Department


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


def require_user(request: Request, db: Session):
    user = get_current_user(request, db)

    if not user:
        return None

    return user


@router.get(
    "/projects",
    response_class=HTMLResponse
)
def project_list(
    request: Request,
    db: Session = Depends(get_db)
):
    user = require_user(request, db)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    projects = (
        db.query(Project)
        .order_by(Project.id.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="projects/list.html",
        context={
            "user": user,
            "projects": projects
        }
    )


@router.get(
    "/projects/new",
    response_class=HTMLResponse
)
def project_create_page(
    request: Request,
    db: Session = Depends(get_db)
):
    user = require_user(request, db)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    users = (
        db.query(User)
        .filter(User.is_active == True)
        .all()
    )

    departments = (
        db.query(Department)
        .order_by(Department.name)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="projects/form.html",
        context={
            "user": user,
            "project": None,
            "users": users,
            "departments": departments
        }
    )


@router.post("/projects/new")
def project_create(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    objectives: str = Form(""),
    outputs: str = Form(""),
    manager_id: int = Form(None),
    owner_department_id: int = Form(None),
    beneficiary: str = Form(""),
    beneficiary_department_id: int = Form(None),
    status: str = Form("NOT_STARTED"),
    progress_percent: float = Form(0),
    db: Session = Depends(get_db)
):
    user = require_user(request, db)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    project = Project(
        title=title,
        description=description,
        objectives=objectives,
        outputs=outputs,
        manager_id=manager_id,
        owner_department_id=owner_department_id,
        beneficiary=beneficiary,
        beneficiary_department_id=beneficiary_department_id,
        status=status,
        progress_percent=progress_percent
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return RedirectResponse(
        url=f"/projects/{project.id}",
        status_code=303
    )


@router.get(
    "/projects/{project_id}",
    response_class=HTMLResponse
)
def project_detail(
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
        name="projects/detail.html",
        context={
            "user": user,
            "project": project
        }
    )


@router.get(
    "/projects/{project_id}/edit",
    response_class=HTMLResponse
)
def project_edit_page(
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

    departments = (
        db.query(Department)
        .order_by(Department.name)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="projects/form.html",
        context={
            "user": user,
            "project": project,
            "users": users,
            "departments": departments
        }
    )


@router.post("/projects/{project_id}/edit")
def project_edit(
    project_id: int,
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    objectives: str = Form(""),
    outputs: str = Form(""),
    manager_id: int = Form(None),
    owner_department_id: int = Form(None),
    beneficiary: str = Form(""),
    beneficiary_department_id: int = Form(None),
    status: str = Form("NOT_STARTED"),
    progress_percent: float = Form(0),
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

    project.title = title
    project.description = description
    project.objectives = objectives
    project.outputs = outputs
    project.manager_id = manager_id
    project.owner_department_id = owner_department_id
    project.beneficiary = beneficiary
    project.beneficiary_department_id = beneficiary_department_id
    project.status = status
    project.progress_percent = progress_percent

    db.commit()

    return RedirectResponse(
        url=f"/projects/{project.id}",
        status_code=303
    )


@router.post("/projects/{project_id}/delete")
def project_delete(
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

    db.delete(project)
    db.commit()

    return RedirectResponse(
        url="/projects",
        status_code=303
    )