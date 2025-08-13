from typing import Annotated

from pydantic import Field

from workout_api.contrib.schemas import BaseSchema, OutMixin


class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description="Nome da categoria", example="Category", max_length=15)]


class CategoriaOut(CategoriaIn, OutMixin):
    pass
