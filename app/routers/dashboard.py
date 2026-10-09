from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.models import Project, SubProject, Issue


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    project_count = db.query(Project).count()
    subproject_count = db.query(SubProject).count()

    open_issues = (
        db.query(Issue)
        .filter(Issue.status == "OPEN")
        .count()
    )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "user": user,
            "project_count": project_count,
            "subproject_count": subproject_count,
            "open_issues": open_issues,
        }
    )