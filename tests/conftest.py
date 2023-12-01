import pytest

from .client import override_get_db, engine


@pytest.fixture
async def db():
    async for session in override_get_db():
        yield session
