from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from workout_api.configs.settings import settings
from typing import AsyncGenerator
engine = create_async_engine(settings.DB_URL, echo=False)
async_session = async_sessionmaker(bind=engine,class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session