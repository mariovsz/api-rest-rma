from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from . import services
from .schemas import Tipo, TipoCreate, TipoUpdate, TipoDelete


router = APIRouter()


@router.get(
    "/",
    response_model=List[Tipo],
    # dependencies=[Depends(permiso_requerido("get_tipos"))]
)
def get_tipos(db: Session = Depends(get_db)):
    return services.get_tipos(db)


@router.post(
    "/",
    response_model=TipoCreate,
    # dependencies=[Depends(permiso_requerido("create_tipos"))]
)
def create_tipos(tipo: TipoCreate, db: Session = Depends(get_db)):
    return services.create_tipos(db, tipo)


@router.put(
    "/{tipo_id}",
    response_model=TipoUpdate,
    # dependencies=[Depends(permiso_requerido("update_tipos"))]
)
def update_tipos(tipo_id: int, tipo: TipoUpdate, db: Session = Depends(get_db)):
    return services.update_tipos(db, tipo_id, tipo)


@router.delete(
    "/{tipo_id}",
    response_model=TipoDelete,
    # dependencies=[Depends(permiso_requerido("delete_tipos"))]
)
def delete_tipos(tipo_id: int, db: Session = Depends(get_db)):
    return services.delete_tipos(db, tipo_id)
