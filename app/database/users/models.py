from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..basemodel import ModeloBase


class User(ModeloBase):
    __tablename__ = "usuarios"

    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    roles: Mapped[list["Role"]] = relationship(  # type:ignore
        "Role", secondary="usuario_roles", back_populates="usuarios"
    )
