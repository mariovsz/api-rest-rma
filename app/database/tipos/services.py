from fastapi import HTTPException
from sqlalchemy.orm import Session

from .schemas import TipoCreate, TipoUpdate, TipoDelete, Tipo as TipoSchema
from .models import Tipo


def get_tipo_or_404(db: Session, tipo_id: int) -> Tipo:
    tipo = Tipo.get(db, tipo_id)
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo no encontrado")
    return tipo


def get_tipo(db: Session, tipo_id: int) -> TipoSchema:
    tipo = get_tipo_or_404(db, tipo_id)
    return TipoSchema.model_validate(tipo)


def get_tipos(db: Session) -> list[TipoSchema]:
    tipos = Tipo.get_all(db)
    return [TipoSchema.model_validate(tipo) for tipo in tipos]


def create_tipos(db: Session, new_tipo: TipoCreate) -> TipoSchema:
    tipo = Tipo.create(db, new_tipo)
    return TipoSchema.model_validate(tipo)


def update_tipos(db: Session, tipo_id: int, tipo_updated) -> TipoSchema:
    tipo = get_tipo_or_404(db, tipo_id)
    tipo.update(db, tipo_updated)
    return TipoSchema.model_validate(tipo)


def delete_tipos(db: Session, tipo_id: int) -> TipoDelete:
    tipo = get_tipo_or_404(db, tipo_id)
    tipo.delete(db)
    return TipoDelete(detail="Tipo eliminado correctamente")
