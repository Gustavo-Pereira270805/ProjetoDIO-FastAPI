from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import UUID4

from workout_api.centro_treinamento.controller import CentroController
from workout_api.centro_treinamento.schemas import CentroIn, CentroOut
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.contrib.models import CentroModel

router = APIRouter(prefix='/centros', tags=['centros'])
centro_controller = CentroController()


@router.post('/',
            summary='cria centro',
            status_code=status.HTTP_201_CREATED,
            response_model=CentroOut)
async def post(db_session: DatabaseDependency,
                centro_in: CentroIn) -> CentroModel:
    return await centro_controller.create(db_session=db_session, centro_in=centro_in)


@router.get('/',
            summary='retorna todos os centros',
            status_code=status.HTTP_200_OK,
            response_model=CentroOut)
async def query(db_session: DatabaseDependency) -> list[CentroModel]:
    return await centro_controller.query(db_session=db_session)


@router.get('/{id}',
            summary='retorna um centro pelo id',
            status_code=status.HTTP_200_OK,
            response_model=CentroOut)
async def get(id: UUID4, db_session: DatabaseDependency) -> Optional[CentroModel]:
    centro = await centro_controller.get(id=id, db_session=db_session)
    if not centro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'centro {id} não encontrado')
    return centro
