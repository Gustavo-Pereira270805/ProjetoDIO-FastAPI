from typing import Annotated

from pydantic import UUID4, BaseModel, ConfigDict, Field


class CategoriaIn(BaseModel):
    nome: Annotated[str, Field(description="Nome da categoria", example="Category", max_length=15)]


class CategoriaOut(CategoriaIn):
    id: Annotated[int, Field(description="Id da categoria")]
    pk_id: Annotated[UUID4, Field(description="Id da categoria(UUID)")]
    model_config = ConfigDict(from_attributes=True)
