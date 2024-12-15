from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from ..basemodel import ModeloBase


class Role(ModeloBase):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    descripcion: Mapped[str] = mapped_column(String)

    usuarios: Mapped[list["User"]] = relationship(  # type: ignore
        "User", secondary="usuario_roles", back_populates="roles"
    )
    permisos: Mapped[list["Permiso"]] = relationship(  # type: ignore
        "Permiso", secondary="role_permisos", back_populates="roles"
    )


class UsuarioRole(ModeloBase):
    __tablename__ = "usuario_roles"

    usuario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True
    )
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    )
