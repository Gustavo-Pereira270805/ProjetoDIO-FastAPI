from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pk_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid4, nullable=False, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )


class AtletaModel(BaseModel):
    __tablename__ = 'atletas'

    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    altura: Mapped[float] = mapped_column(Float, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)

    categoria_id: Mapped[int] = mapped_column(ForeignKey('categorias.id'))
    categoria: Mapped['CategoriaModel'] = relationship(
        back_populates='atletas'
    )

    centro_treinamento_id: Mapped[int] = mapped_column(
        ForeignKey('centros.id')
    )
    centro_treinamento: Mapped['CentroModel'] = relationship(
        back_populates='atletas'
    )


class CategoriaModel(BaseModel):
    __tablename__ = 'categorias'
    nome: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    atletas: Mapped[list['AtletaModel']] = relationship(
        back_populates='categoria'
    )


class CentroModel(BaseModel):
    __tablename__ = 'centros'
    nome: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    endereco: Mapped[str] = mapped_column(String(70), nullable=False)
    proprietario: Mapped[str] = mapped_column(String(30), nullable=False)

    atletas: Mapped[list['AtletaModel']] = relationship(
        back_populates='centro_treinamento'
    )
