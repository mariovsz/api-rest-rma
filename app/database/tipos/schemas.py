from pydantic import BaseModel


class TipoBase(BaseModel):
    data_type: int
    data_symbol: str
    nombre: str


class TipoCreate(TipoBase):
    pass


class TipoUpdate(TipoBase):
    pass


class Tipo(TipoBase):
    id: int
    model_config = {"from_attributes": True}


class TipoDelete(BaseModel):
    detail: str
