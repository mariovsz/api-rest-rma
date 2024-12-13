from fastapi import HTTPException
from sqlalchemy.orm import Session
from .models import User


def get_user_or_404(db: Session, user_id: int) -> User:
    user = User.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
