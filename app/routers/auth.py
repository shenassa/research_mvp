from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import authenticate_user


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get(
    "/login",
    response_class=HTMLResponse
)
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = authenticate_user(
        db,
        username,
        password
    )

    if not user:

        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": "نام کاربری یا رمز عبور اشتباه است."
            },
            status_code=401
        )

    request.session["user_id"] = user.id

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )


@router.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/login",
        status_code=303
    )