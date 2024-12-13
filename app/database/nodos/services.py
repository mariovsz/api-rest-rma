from typing import List

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from ..paquetes.models import Paquete, PaqueteArchivo
from .models import Nodo
from .schemas import Nodo as NodoSchema
from .schemas import NodoCreate, NodoDelete, NodoUpdate


def get_nodo_or_404(db: Session, nodo_id: int) -> Nodo:
    nodo = Nodo.get(db, nodo_id)
    if not nodo:
        raise HTTPException(status_code=404, detail="Nodo no encontrado")
    return nodo


def listar_nodos(db: Session) -> List[NodoSchema]:
    nodos = Nodo.filter(db, is_active=True)
    return [NodoSchema.model_validate(nodo) for nodo in nodos]


def listar_nodos_inactivos(db: Session) -> List[NodoSchema]:
    nodos = Nodo.filter(db, is_active=False)
    return [NodoSchema.model_validate(nodo) for nodo in nodos]


def get_nodo(db: Session, nodo_id: int) -> NodoSchema:
    nodo = get_nodo_or_404(db, nodo_id)
    if not nodo.is_active:
        raise HTTPException(status_code=400, detail="Nodo no está activo")
    return NodoSchema.model_validate(nodo)


def crear_nodo(db: Session, new_nodo: NodoCreate) -> NodoSchema:
    nodo = Nodo.create(db, new_nodo)
    return NodoSchema.model_validate(nodo)


def modificar_nodo(db: Session, nodo_id: int, updated_nodo: NodoUpdate) -> NodoSchema:
    nodo = get_nodo_or_404(db, nodo_id)
    nodo.update(db, updated_nodo)
    return NodoSchema.model_validate(nodo)


def delete_nodo(db: Session, nodo_id: int) -> NodoDelete:
    nodo = get_nodo_or_404(db, nodo_id)
    if not nodo.is_active:
        raise HTTPException(status_code=400, detail="El nodo ya está inactivo")
    paquetes = Paquete.filter(db, nodo_id=nodo_id)
    cantidad_paquetes = len(paquetes)
    paquete_archivo = [PaqueteArchivo.from_paquete(paquete) for paquete in paquetes]
    db.bulk_save_objects(paquete_archivo)
    subquery = select(Paquete.id).filter(Paquete.nodo_id == nodo_id)
    db.execute(delete(Paquete).where(Paquete.id.in_(subquery)))
    nodo.is_active = False
    nodo.save(db)
    db.commit()
    return NodoDelete(
        detail=f"Nodo {nodo_id} desactivado, {cantidad_paquetes} paquetes archivados"
    )


def activate_nodo(db: Session, nodo_id: int) -> NodoSchema:
    nodo = get_nodo_or_404(db, nodo_id)
    if nodo.is_active:
        raise HTTPException(status_code=400, detail="El nodo ya está activo")
    nodo.is_active = True
    nodo.save(db)
    db.commit()
    return NodoSchema.model_validate(nodo)
