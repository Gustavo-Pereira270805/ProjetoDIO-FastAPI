from typing import Annotated, Optional
from pydantic import Field, BaseModel, UUID4

class AtletaSchema(BaseModel): 
    nome : Annotated[str, Field(description = "Nome do atleta", example = "Gustavo", max_lenght = 50)]
    cpf : Annotated[str, Field(description = 'cpf do atleta', example = '12345678901', max_lenght = 11)]
    idade: Annotated[int, Field(description='Idade do atleta', example=25)]
    peso: Annotated[float, Field(description='Peso do atleta', example=75.5)]
    altura: Annotated[float, Field(description='Altura do atleta', example=1.70)]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_length=1)]

class AtletaIn(AtletaSchema):
    pass

class AtletaOut(AtletaIn):
    id : Annotated[int, Field(description = "Id do atleta")]
    pk_id : Annotated[UUID4, Field(description = "Id do atleta(UUID)")]

class AtletaUpdate(BaseModel):
    nome : Annotated[Optional[str], Field(None, description = "Nome do atleta", example = "Gustavo", max_lenght = 50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example=25)]