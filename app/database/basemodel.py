from pydantic import BaseModel as Schema
from datetime import datetime
from sqlalchemy import update, Column, Integer, DateTime
from sqlalchemy.orm import Session, declarative_base, mapped_column, Mapped
from sqlalchemy.sql import func


Base = declarative_base()


# Autor original: https://stackoverflow.com/a/54034230
def keyvalgen(obj):
    """Genera pares nombre/valor, quitando/filtrando los atributos de SQLAlchemy."""
    excl = ("_sa_adapter", "_sa_instance_state")
    for k, v in vars(obj).items():
        if not k.startswith("_") and not any(hasattr(v, a) for a in excl):
            yield k, v


class ModeloBase(Base):
    """Modelo base para los módulos de nuestra app."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    def save(self, db: Session):
        try:
            db.add(self)
            db.commit()
            db.refresh(self)
            return self
        except Exception as e:
            db.rollback()
            raise e

    def delete(self, db: Session):
        try:
            db.delete(self)
            db.commit()
            return self
        except Exception as e:
            db.rollback()
            raise e

    def update(self, db: Session, schema: Schema):
        try:
            primary_key = self.id
            stmt = (
                update(self.__class__)
                .where(self.__class__.id == primary_key)
                .values(**schema.model_dump(exclude_unset=True))
            )
            db.execute(stmt)
            return self.save(db)
        except Exception as e:
            db.rollback()
            raise e

    @classmethod
    def create(cls, db: Session, schema: Schema):
        try:
            instance = cls(**schema.model_dump())
            return instance.save(db)
        except Exception as e:
            db.rollback()
            raise e

    @classmethod
    def get(cls, db: Session, id: int):
        return db.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_all(cls, db: Session):
        return db.query(cls).all()

    @classmethod
    def filter(cls, db: Session, **kwargs):
        query = db.query(cls)
        for key, value in kwargs.items():
            if hasattr(cls, key):
                query = query.filter(getattr(cls, key) == value)
        return query.all()

    @classmethod
    def find_first(cls, db: Session, **kwargs):
        query = db.query(cls)
        for key, value in kwargs.items():
            if hasattr(cls, key):
                query = query.filter(getattr(cls, key) == value)
        return query.first()

    def __repr__(self):
        params = ", ".join(f"{k}={v}" for k, v in keyvalgen(self))
        return f"{self.__class__.__name__}({params})"
