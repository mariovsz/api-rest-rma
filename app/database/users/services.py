from email_validator import EmailNotValidError, validate_email
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .models import User
from typing import List
from .schemas import UserCreate, UserUpdate, UserDelete, User as UserSchema
from datetime import datetime


def validar_correo(correo: str) -> str:
    try:
        valid = validate_email(correo, check_deliverability=True)
        return valid.email
    except EmailNotValidError as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_user_or_404(db: Session, user_id: int) -> User:
    user = User.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


def actualizar_last_login(db: Session, user_id: int) -> User:
    user = get_user_or_404(db, user_id)
    user.last_login = datetime.now()
    user.save(db)
    return user


def get_user(db: Session, user_id: int) -> UserSchema:
    user = get_user_or_404(db, user_id)
    return UserSchema.model_validate(user)


def get_users(db: Session) -> List[UserSchema]:
    users = User.get_all(db)
    return [UserSchema.model_validate(user) for user in users]


def create_user(db: Session, new_user: UserCreate) -> UserSchema:
    new_user.email = validar_correo(new_user.email)
    user = User.create(db, new_user)
    return UserSchema.model_validate(user)


def update_user(db: Session, user_id: int, user_updated: UserUpdate) -> UserSchema:
    if user_updated.email:
        user_updated.email = validar_correo(user_updated.email)
    user = get_user_or_404(db, user_id)
    user.update(db, user_updated)
    return UserSchema.model_validate(user)


def delete_user(db: Session, user_id: int) -> UserDelete:
    user = get_user_or_404(db, user_id)
    user.delete(db)
    return UserDelete(detail="Usuario eliminado correctamente")


def update_user_status(db: Session, user_id: int, is_active: bool) -> UserSchema:
    user = get_user_or_404(db, user_id)
    user.is_active = is_active
    user.update(db, user)
    return UserSchema.model_validate(user)
