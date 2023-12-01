from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

from ifsguid import models
from ifsguid.main import app
from ifsguid.endpoints import get_db

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine: AsyncEngine = create_async_engine(DATABASE_URL)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)


async def override_get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
