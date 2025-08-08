from fastapi import APIRouter

from workout_api.atleta.router import router as atleta_router
from workout_api.categoria.router import router as categoria_router
from workout_api.centro_treinamento.router import router as centro_router

api_router = APIRouter()
api_router.include_router(atleta_router, prefix='/atletas', tags=['atletas'])
api_router.include_router(categoria_router, prefix='/categorias', tags=['categorias'])
api_router.include_router(centro_router, prefix='/centros', tags=['centros'])
