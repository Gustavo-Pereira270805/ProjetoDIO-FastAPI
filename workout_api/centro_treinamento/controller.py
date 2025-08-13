from typing import Optional, Sequence

from pydantic import UUID4
from sqlalchemy.future import select

from workout_api.centro_treinamento.schemas import CentroTreinamentoIn
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.contrib.models import CentroTreinamentoModel


class CentroController:
    async def create(self,
                    db_session: DatabaseDependency,
                    centro_in: CentroTreinamentoIn) -> CentroTreinamentoModel:
        centro = CentroTreinamentoModel(**centro_in.model_dump())
        db_session.add(centro)
        await db_session.commit()
        await db_session.refresh(centro)
        return centro

    async def get(self,
                  id: UUID4,
                  db_session: DatabaseDependency) -> Optional[CentroTreinamentoModel]:
        query = select(CentroTreinamentoModel).filter_by(id=id)
        result = await db_session.execute(query)
        return result.scalar_one_or_none()

    async def query(self, db_session: DatabaseDependency) -> list[CentroTreinamentoModel]:
        query = select(CentroTreinamentoModel)
        result = await db_session.execute(query)
        centros: Sequence[CentroTreinamentoModel] = result.scalars().all()
        return list(centros)
