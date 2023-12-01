import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from . import client


@pytest_asyncio.fixture()
async def db() -> AsyncSession:
    async with client.async_session() as session:
        await client.create_tables()
        yield session
        await client.drop_tables()
