from typing import Annotated

from pydantic import UUID4, BaseModel, ConfigDict, Field


class CentroIn(BaseModel):
    nome: Annotated[str, Field(description="Nome do centro", example="Centro", max_length=15)]
    endereco: Annotated[str, Field(description='endereco do centro', example='rua taltal', max_length=70)]
    proprietario: Annotated[str, Field(description='proprietario do centro', example='gustavo', max_length=30)]


class CentroOut(CentroIn):
    id: Annotated[int, Field(description="Id do centro")]
    pk_id: Annotated[UUID4, Field(description="Id do centro(UUID)")]
    model_config = ConfigDict(from_attributes=True)
