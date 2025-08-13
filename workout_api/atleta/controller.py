from typing import Optional, Sequence

from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from workout_api.atleta.schemas import AtletaIn, AtletaUpdate
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.contrib.models import (
    AtletaModel,
    CategoriaModel,
    CentroTreinamentoModel,
)


class AtletaController:
    async def create(self,
                    db_session: DatabaseDependency,
                    atleta_in: AtletaIn,
                    ) -> AtletaModel:
        categoria_nome = atleta_in.categoria
        centro_nome = atleta_in.centro_treinamento

        query_categoria = select(CategoriaModel).filter_by(nome=categoria_nome)
        result_cat = await db_session.execute(query_categoria)
        categoria = result_cat.scalar_one_or_none()

        if not categoria:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'categoria {categoria_nome} não encontrada')

        query_centro = select(CentroTreinamentoModel).filter_by(nome=centro_nome)
        result_centro = await db_session.execute(query_centro)
        centro = result_centro.scalar_one_or_none()

        if not centro:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                               detail=f'centro {centro_nome} não encontrado')
        try:

            atleta_data = atleta_in.model_dump(exclude={'categoria', 'centro_treinamento'})
            atleta = AtletaModel(**atleta_data, categoria=categoria, centro_treinamento=centro)

            db_session.add(atleta)
            await db_session.commit()

            await db_session.refresh(atleta)
        except Exception as e:

            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

        return await self.get(id=atleta.pk_id, db_session=db_session)

    async def get(self, id: UUID4,
                db_session: DatabaseDependency) -> Optional[AtletaModel]:

        query = select(AtletaModel).options(selectinload(AtletaModel.categoria),
                                            selectinload(AtletaModel.centro_treinamento)).filter_by(pk_id=id)
        result = await db_session.execute(query)
        return result.scalar_one_or_none()

    async def query(self, db_session: DatabaseDependency) -> list[AtletaModel]:

        query = select(AtletaModel).options(selectinload(AtletaModel.categoria), selectinload(AtletaModel.centro_treinamento))
        result = await db_session.execute(query)
        atletas: Sequence[AtletaModel] = result.scalars().all()
        return list(atletas)

    async def update(self,
                    id: UUID4,
                    db_session: DatabaseDependency,
                    atleta_update: AtletaUpdate) -> Optional[AtletaModel]:

        atleta = await self.get(id, db_session)

        if not atleta:
            return None

        atleta_update_data = atleta_update.model_dump(exclude_unset=True)
        for key, value in atleta_update_data.items():
            setattr(atleta, key, value)

        await db_session.commit()
        await db_session.refresh(atleta)
        return atleta

    async def delete(self,
                    id: UUID4,
                    db_session: DatabaseDependency) -> None:

        atleta = await self.get(id, db_session)
        if not atleta:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta not found")

        await db_session.delete(atleta)
        await db_session.commit()
