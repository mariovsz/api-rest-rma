from typing import List, Optional

from sqlalchemy import Float, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..basemodel import ModeloBase


class Nodo(ModeloBase):
    __tablename__ = "nodos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    identificador: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String, unique=True, index=True)
    descripcion: Mapped[str] = mapped_column(String, index=True)
    latitud: Mapped[float] = mapped_column(Float, index=True, nullable=True)
    longitud: Mapped[float] = mapped_column(Float, index=True, nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, index=True, nullable=True, default=True
    )

    # Relación con Paquete
    paquetes: Mapped[List["Paquete"]] = relationship(  # type: ignore
        "Paquete",
        back_populates="nodo",
    )
