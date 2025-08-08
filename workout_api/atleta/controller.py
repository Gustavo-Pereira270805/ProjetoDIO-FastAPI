from typing import Optional, Sequence
from uuid import uuid4
from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select

from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.contrib.models import AtletaModel
from workout_api.contrib.dependencies import DatabaseDependency



class AtletaController:
    async def create(self,
                    db_session: DatabaseDependency,
                    atleta_in: AtletaIn,
                    ) -> AtletaModel:
        atleta_data = atleta_in.model_dump()
        atleta = AtletaModel(**atleta_data)

        db_session.add(atleta)
        await db_session.commit()
        await db_session.refresh(atleta)

        return atleta
    
    async def get(self, id: UUID4,
                db_session : DatabaseDependency) -> Optional[AtletaModel]:
        
        query = select(AtletaModel).filter_by(id = id)
        result = await db_session.execute(query)
        return result.scalar_one_or_none()
    
    async def query(self, db_session : DatabaseDependency) -> list[AtletaModel]:
        
        query = select(AtletaModel)
        result = await db_session.execute(query)
        atletas : Sequence[AtletaModel] = result.scalars().all()
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