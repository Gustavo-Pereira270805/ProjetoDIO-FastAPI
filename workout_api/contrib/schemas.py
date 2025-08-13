# workout_api/contrib/schemas.py
from datetime import datetime
from typing import Annotated

from pydantic import UUID4, BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    """
    Schema base que habilita o modo ORM para todos os schemas que herdarem dele.
    """
    model_config = ConfigDict(from_attributes=True)


class OutMixin(BaseSchema):
    """
    Mixin que adiciona os campos comuns de saída (id, pk_id, created_at).
    """
    id: Annotated[int, Field(description="Identificador")]
    pk_id: Annotated[UUID4, Field(description="Identificador único (UUID)")]
    created_at: Annotated[datetime, Field(description="Data de criação")]
