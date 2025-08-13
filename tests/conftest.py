# tests/conftest.py
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from main import app
from workout_api.configs.database import get_session
from workout_api.configs.settings import settings
from workout_api.contrib.models import (
    Base,
    CategoriaModel,
    CentroTreinamentoModel,
)

# --- Configuração do Banco de Dados e Override ---
engine_test = create_async_engine(settings.DB_URL_TEST)
async_session_test = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session", autouse=True)
def apply_overrides():
    app.dependency_overrides[get_session] = override_get_session


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_test() as session:
        yield session


# --- Fixtures de Setup e Teardown ---
@pytest_asyncio.fixture(autouse=True)
async def clear_db() -> AsyncGenerator[None, None]:
    """Fixture para limpar e recriar as tabelas a cada teste."""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture
async def client(clear_db) -> AsyncGenerator[AsyncClient, None]:
    """Fixture que fornece um cliente HTTP para os testes."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


# --- Fixtures de Dados ---
@pytest.fixture
def categoria_in() -> dict:
    return {"nome": "Scale"}


@pytest.fixture
def centro_treinamento_in() -> dict:
    return {"nome": "CT King", "endereco": "Rua A, 123", "proprietario": "Rei"}


@pytest_asyncio.fixture
async def categoria_db(db_session: AsyncSession, categoria_in: dict) -> CategoriaModel:
    """Cria e insere uma categoria no banco de teste."""
    categoria = CategoriaModel(**categoria_in)
    db_session.add(categoria)
    await db_session.commit()
    await db_session.refresh(categoria)
    return categoria


@pytest_asyncio.fixture
async def centro_treinamento_db(db_session: AsyncSession, centro_treinamento_in: dict) -> CentroTreinamentoModel:
    """Cria e insere um centro de treinamento no banco de teste."""
    centro = CentroTreinamentoModel(**centro_treinamento_in)
    db_session.add(centro)
    await db_session.commit()
    await db_session.refresh(centro)
    return centro


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Fixture que fornece uma sessão de banco de dados para criar dados de teste."""
    async with async_session_test() as session:
        yield session
