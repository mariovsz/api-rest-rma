from datetime import datetime
from typing import List

from pydantic import BaseModel


class PaqueteBase(BaseModel):
    nodo_id: int
    data: float
    date: datetime
    type_id: int
    model_config = {"from_attributes": True}


class Paquete(PaqueteBase):
    id: int


class PaqueteArchivo(PaqueteBase):
    id: int


class PaqueteCreate(PaqueteBase):
    pass


class PaginationInfo(BaseModel):
    total_items: int
    total_pages: int
    current_page: int
    limit: int
    offset: int


class PaqueteResponse(BaseModel):
    info: PaginationInfo
    items: List[Paquete]


class PaqueteArchivoResponse(BaseModel):
    info: PaginationInfo
    items: List[PaqueteArchivo]


class PaqueteRechazado(PaqueteBase):
    motivo: str
