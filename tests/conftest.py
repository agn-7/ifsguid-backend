import pytest

from . import client


@pytest.fixture
async def db():
    async with client.async_session() as session:
        await client.create_tables()
        yield session
        await client.drop_tables()
