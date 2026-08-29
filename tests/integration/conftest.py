import os
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.db.base import Base
from app.db.models import Document  # noqa: F401
from app.db.session import get_db_session
from app.main import app

TEST_DB_URL = os.environ["TEST_DB_URL"]

test_engine = create_async_engine(TEST_DB_URL, poolclass=NullPool)
test_session_maker = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
)


@pytest.fixture(autouse=True)
async def _setup_db() -> AsyncGenerator[None, None]:
    """Create tables before each test, drop after — clean isolation."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def _get_test_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a test session."""
    async with test_session_maker() as session:
        yield session


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """HTTP client with DB dependency overridden to the test database."""
    app.dependency_overrides[get_db_session] = _get_test_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()
