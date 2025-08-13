from typing import Annotated, Optional

from pydantic import Field

from workout_api.categoria.schemas import CategoriaOut
from workout_api.centro_treinamento.schemas import CentroTreinamentoOut
from workout_api.contrib.schemas import BaseSchema, OutMixin


class AtletaSchema(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", example="Gustavo", max_length=50)]
    cpf: Annotated[str, Field(description='cpf do atleta', example='12345678901', max_length=11)]
    idade: Annotated[int, Field(description='Idade do atleta', example=25)]
    peso: Annotated[float, Field(description='Peso do atleta', example=75.5)]
    altura: Annotated[float, Field(description='Altura do atleta', example=1.70)]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_length=1)]


class AtletaIn(AtletaSchema):
    categoria: Annotated[str, Field(description="Categoria do atleta", example='judo', max_length=15)]
    centro_treinamento: Annotated[str, Field(description="Centro de treinamento do atleta", example='centro', max_length=20)]


class AtletaOut(AtletaSchema, OutMixin):
    categoria: Annotated[CategoriaOut, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoOut, Field(description='Centro de treinamento do atleta')]


class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description="Nome do atleta", example="Gustavo", max_lenght=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example=25)]
