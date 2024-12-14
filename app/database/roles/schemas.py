from pydantic import BaseModel
from pydantic import field_validator
from typing import Optional


class RoleBase(BaseModel):
    name: str
    descripcion: Optional[str] = None

    @field_validator("name")
    def validate_name_length(cls, v):
        if len(v) < 3:
            raise ValueError("El nombre del rol debe tener al menos 3 caracteres.")
        return v


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class Role(RoleBase):
    id: int
    model_config = {"from_attributes": True}


class RoleDelete(BaseModel):
    detail: str


class UsuarioRoleBase(BaseModel):
    usuario_id: int
    role_id: int


class UsuarioRoleCreate(UsuarioRoleBase):
    pass


class UsuarioRole(UsuarioRoleBase):
    id: int
    model_config = {"from_attributes": True}


class UsuarioRoleDelete(BaseModel):
    detail: str
