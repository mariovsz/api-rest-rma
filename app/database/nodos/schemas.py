from typing import List, Optional
from pydantic import BaseModel
from ..paquetes.schemas import Paquete
from datetime import datetime


class NodoBase(BaseModel):
    identificador: int
    nombre: str
    latitud: Optional[float]
    longitud: Optional[float]
    descripcion: Optional[str]


class NodoCreate(NodoBase):
    pass


class NodoUpdate(NodoBase):
    pass


class Nodo(NodoBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}


class NodoDelete(BaseModel):
    detail: str
    model_config = {"from_attributes": True}


class NodoPaquetes(Nodo):
    paquetes: List[Paquete]
