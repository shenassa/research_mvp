from fastapi import Request, HTTPException
from sqlalchemy.orm import Session

from app.models import User
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def authenticate_user(
    db: Session,
    username: str,
    password: str
):
    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if not user:
        return None

    if not user.is_active:
        return None

    if not password_hash.verify(password, user.password_hash):
        return None

    return user


def get_current_user(
    request: Request,
    db: Session
):
    user_id = request.session.get("user_id")

    if not user_id:
        return None

    user = db.query(User).filter(User.id == user_id).first()

    if not user or not user.is_active:
        return None

    return user