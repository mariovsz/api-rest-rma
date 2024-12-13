from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from ..basemodel import ModeloBase
from ..roles.models import Role


class Permiso(ModeloBase):
    __tablename__ = "permisos"

    identificador: Mapped[str] = mapped_column(String(50), unique=True)
    descripcion: Mapped[str] = mapped_column(String(50), unique=True)

    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="role_permisos",
        back_populates="permisos",
    )


class RolePermiso(ModeloBase):
    __tablename__ = "role_permisos"

    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    )
    permiso_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("permisos.id", ondelete="CASCADE"),
        primary_key=True,
    )
