from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from . import services
from .schemas import UserCreate, UserUpdate, UserDelete, User
from ..database import get_db


router = APIRouter()


@router.get(
    "/",
    response_model=List[User],
    # dependencies=[Depends(permiso_requerido("get_users"))],
)
def list_users(db: Session = Depends(get_db)):
    return services.get_users(db)


@router.get(
    "/{user_id}",
    response_model=User,
    # dependencies=[Depends(permiso_requerido("get_users"))],
)
def retrieve_user(user_id: int, db: Session = Depends(get_db)):
    return services.get_user(db, user_id)


@router.post(
    "/",
    response_model=User,
    # dependencies=[Depends(permiso_requerido("create_users"))],
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return services.create_user(db, user)


@router.put(
    "/{user_id}",
    response_model=User,
    # dependencies=[Depends(permiso_requerido("update_users"))],
)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return services.update_user(db, user_id, user)


@router.delete(
    "/{user_id}",
    response_model=UserDelete,
    # dependencies=[Depends(permiso_requerido("delete_users"))],
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return services.delete_user(db, user_id)


@router.put(
    "/{user_id}/status",
    response_model=User,
    # dependencies=[Depends(permiso_requerido("update_users"))],
)
def change_user_status(user_id: int, is_active: bool, db: Session = Depends(get_db)):
    return services.update_user_status(db, user_id, is_active)
