from typing import Annotated

from pydantic import Field

from workout_api.contrib.schemas import BaseSchema, OutMixin


class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro", example="Centro", max_length=15)]
    endereco: Annotated[str, Field(description='endereco do centro', example='rua taltal', max_length=70)]
    proprietario: Annotated[str, Field(description='proprietario do centro', example='gustavo', max_length=30)]


class CentroTreinamentoOut(CentroTreinamentoIn, OutMixin):
    pass
