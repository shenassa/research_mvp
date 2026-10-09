from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.database import Base, engine
from app import models
from app.routers.auth import router as auth_router
from app.routers.dashboard import router as dashboard_router
from app.routers.projects import router as projects_router
from app.routers.subprojects import router as subprojects_router
from app.routers.participants import router as participants_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="سامانه مدیریت کلان‌پروژه‌ها",
    version="0.1.0"
)

app.add_middleware(
    SessionMiddleware,
    secret_key="CHANGE_THIS_SECRET_KEY"
)

app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(projects_router)
app.include_router(subprojects_router)
app.include_router(participants_router)

@app.get("/")
def root():
    return {
        "message": "Project Management System is running"
    }