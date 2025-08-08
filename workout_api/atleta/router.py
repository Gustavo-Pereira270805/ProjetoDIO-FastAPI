from uuid import uuid4
from fastapi import APIRouter, Body, status, HTTPException
from pydantic import UUID4

from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.atleta.controller import AtletaController
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter(prefix='/atletas', tags=['atletas'])
atleta_controller = AtletaController()


@router.post('/', summary='Criar atleta', 
             status_code=status.HTTP_201_CREATED,
             response_model = AtletaOut)
async def post(db_session: DatabaseDependency,
               atleta_in: AtletaIn = Body(...)):
    try:
        return await atleta_controller.create(db_session = db_session, atleta_in=atleta_in) 
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail = str(e))

@router.get(
        '/', 
        summary='consultar todos os atletas', 
        status_code=status.HTTP_200_OK,
        response_model = list[AtletaOut]) 
async def query(db_session : DatabaseDependency,
                atleta_in: AtletaIn = Body(...)):
    return await atleta_controller.query(db_session = db_session)

@router.get(
        '/{id}', 
        summary='consultar um atleta por id', 
        status_code=status.HTTP_200_OK,
        response_model = AtletaOut)
async def get(id: UUID4, db_session : DatabaseDependency) -> AtletaOut:
    atleta = await atleta_controller.get(id = id, db_session = db_session)

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'Atleta {id} não encontrado')
    return atleta

@router.patch('/{id}',
              summary= 'Editar um atleta pelo id',
              status_code=status.HTTP_200_OK,
              response_model=AtletaOut
)
async def patch(id: UUID4, db_session : DatabaseDependency, atleta_up : AtletaUpdate = Body(...)) -> AtletaOut:
    atleta = await atleta_controller.update(id = id, db_session = db_session, atleta_up = atleta_up)

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'Atleta {id} não encontrado')
    return atleta

@router.delete('/{id}',
               summary= 'Deletar um atleta pelo id',
               status_code=status.HTTP_204_NO_CONTENT
)
async def delete(id: UUID4, db_session : DatabaseDependency) -> None:
    try: 
        await atleta_controller.delete(id = id, db_session = db_session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'atleta {id} não encontrado')
    