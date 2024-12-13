from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..basemodel import ModeloBase


class Tipo(ModeloBase):
    __tablename__ = "tipos"
    data_type: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    data_symbol: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True, index=True)
