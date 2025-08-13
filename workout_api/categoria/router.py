from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import UUID4

from workout_api.categoria.controller import CategoriaController
from workout_api.categoria.schemas import CategoriaIn, CategoriaOut
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.contrib.models import CategoriaModel

router = APIRouter(tags=['categorias'])
categoria_controller = CategoriaController()


@router.post('/',
            summary='Criar categoria',
            status_code=status.HTTP_201_CREATED,
            response_model=CategoriaOut)
async def post(db_session: DatabaseDependency,
               categoria_in: CategoriaIn) -> CategoriaModel:
    return await categoria_controller.create(db_session=db_session, categoria_in=categoria_in)


@router.get('/{id}',
            summary='Consultar uma categoria',
            status_code=status.HTTP_200_OK,
            response_model=CategoriaOut)
async def get(id: UUID4, db_session: DatabaseDependency) -> Optional[CategoriaModel]:
    categoria = await categoria_controller.get(id=id, db_session=db_session)
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Categoria {id} não encontrada')
    return categoria


@router.get('/',
            summary='Consultar todas as categorias',
            status_code=status.HTTP_200_OK,
            response_model=list[CategoriaOut])
async def query(db_session: DatabaseDependency) -> list[CategoriaModel]:
    return await categoria_controller.query(db_session=db_session)
