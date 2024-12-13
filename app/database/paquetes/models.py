from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..basemodel import ModeloBase
from ..nodos.models import Nodo
from ..tipos.models import Tipo


class Paquete(ModeloBase):
    __tablename__ = "paquetes"

    nodo_id: Mapped[int] = mapped_column(ForeignKey("nodos.identificador"))
    data: Mapped[float] = mapped_column(Float, index=True)
    type_id: Mapped[int] = mapped_column(ForeignKey("tipos.data_type"))
    date: Mapped[datetime] = mapped_column(DateTime, index=True)

    type: Mapped[Tipo] = relationship(Tipo)
    nodo: Mapped[Nodo] = relationship(Nodo, back_populates="paquetes")


class PaqueteRechazado(ModeloBase):
    __tablename__ = "paquetes_rechazados"

    nodo_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    date: Mapped[datetime] = mapped_column(DateTime, primary_key=True, index=True)
    data: Mapped[float] = mapped_column(Integer, index=True)
    type_id: Mapped[int] = mapped_column(Integer, index=True)
    motivo: Mapped[str] = mapped_column(String, index=True)


class PaqueteArchivo(ModeloBase):
    __tablename__ = "paquetes_archivo"

    data: Mapped[float] = mapped_column(Float, index=True)
    type_id: Mapped[int] = mapped_column(ForeignKey("tipos.data_type"))
    date: Mapped[datetime] = mapped_column(DateTime, index=True)
    nodo_id: Mapped[int] = mapped_column(Integer, index=True)
    type: Mapped[Tipo] = relationship(Tipo)

    @classmethod
    def from_paquete(cls, paquete: Paquete):
        return cls(
            data=paquete.data,
            type_id=paquete.type_id,
            date=paquete.date,
            nodo_id=paquete.nodo_id,
        )
