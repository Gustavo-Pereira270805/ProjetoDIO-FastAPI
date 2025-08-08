from typing import Optional, Sequence

from pydantic import UUID4
from sqlalchemy.future import select

from workout_api.categoria.schemas import CategoriaIn
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.contrib.models import CategoriaModel


class CategoriaController:
    async def create(self, db_session: DatabaseDependency, categoria_in: CategoriaIn) -> CategoriaModel:
        categoria = CategoriaModel(**categoria_in.model_dump())
        db_session.add(categoria)
        await db_session.commit()
        await db_session.refresh(categoria)
        return categoria

    async def get(self, id: UUID4, db_session: DatabaseDependency) -> Optional[CategoriaModel]:
        query = select(CategoriaModel).filter_by(id=id)
        result = await db_session.execute(query)
        return result.scalar_one_or_none()

    async def query(self, db_session: DatabaseDependency) -> list[CategoriaModel]:
        query = select(CategoriaModel)
        result = await db_session.execute(query)
        categorias: Sequence[CategoriaModel] = result.scalars().all()
        return list(categorias)
