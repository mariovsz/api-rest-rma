from pydantic import BaseModel


class PermisoBase(BaseModel):
    identificador: str
    descripcion: str


class PermisoCreate(PermisoBase):
    pass


class Permiso(PermisoBase):
    id: int
    model_config = {"from_attributes": True}


class RolePermisoBase(BaseModel):
    role_id: int
    permiso_id: int


class RolePermisoCreate(RolePermisoBase):
    pass


class RolePermiso(RolePermisoBase):
    id: int
    model_config = {"from_attributes": True}


class RolePermisoDelete(BaseModel):
    detail: str
    model_config = {"from_attributes": True}
