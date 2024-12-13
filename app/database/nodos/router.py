from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from . import schemas, services


router = APIRouter()


@router.get(
    "/{nodo_id}",
    response_model=schemas.Nodo,
    # dependencies=[Depends(permiso_requerido("read_nodos"))],
)
def read_nodo(nodo_id: int, db: Session = Depends(get_db)):
    return services.get_nodo(db, nodo_id)


@router.get(
    "/",
    response_model=list[schemas.Nodo],
    # dependencies=[Depends(permiso_requerido("read_nodos"))],
)
def read_nodos(db: Session = Depends(get_db)):
    return services.listar_nodos(db)


@router.post(
    "/",
    response_model=schemas.Nodo,
    # dependencies=[Depends(permiso_requerido("create_nodos"))],
)
def create_nodo(nodo: schemas.NodoCreate, db: Session = Depends(get_db)):
    return services.crear_nodo(db, nodo)


@router.put(
    "/{nodo_id}",
    response_model=schemas.Nodo,
    # dependencies=[Depends(permiso_requerido("update_nodos"))],
)
def update_nodo(nodo_id: int, nodo: schemas.NodoUpdate, db: Session = Depends(get_db)):
    return services.modificar_nodo(db, nodo_id, nodo)


@router.delete(
    "/{nodo_id}",
    response_model=schemas.NodoDelete,
    # dependencies=[Depends(permiso_requerido("delete_nodos"))],
)
def delete_nodo(nodo_id: int, db: Session = Depends(get_db)):
    return services.delete_nodo(db, nodo_id)


@router.put(
    "/activar/{nodo_id}",
    response_model=schemas.Nodo,
    # dependencies=[Depends(permiso_requerido("activar_nodos"))],
)
def revivir_nodo(nodo_id: int, db: Session = Depends(get_db)):
    return services.activate_nodo(db, nodo_id)


@router.get(
    "/inactivos/",
    response_model=list[schemas.Nodo],
    # dependencies=[Depends(permiso_requerido("read_nodos_inactivos"))],
)
def read_nodos_inactivos(db: Session = Depends(get_db)):
    return services.listar_nodos_inactivos(db)
