from uuid import uuid4
from fastapi import APIRouter, Body, status
from pydantic import UUID4

from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate

class AtletaController:
    async def create(self, atleta_in: AtletaIn) -> AtletaOut:
        pass

    async def get(self, id: UUID4) -> AtletaOut:
        pass

    async def query(self) -> list[AtletaOut]:
        pass

    async def update(self, id: UUID4, atleta_update: AtletaUpdate) -> AtletaOut:
        pass

    async def delete(self, id: UUID4) -> None:
        pass