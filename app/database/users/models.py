from sqlalchemy import Boolean, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from ..basemodel import ModeloBase
from typing import List


class User(ModeloBase):
    __tablename__ = "usuarios"

    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)

    full_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    profile_image: Mapped[str] = mapped_column(String(255), nullable=True)

    roles: Mapped[List["Role"]] = relationship(  # type: ignore
        "Role", secondary="usuario_roles", back_populates="usuarios"
    )
