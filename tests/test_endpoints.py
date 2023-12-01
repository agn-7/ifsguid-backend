import pytest

from ifsguid import models
from . import client


### Integration Tests ###


def test_get_root():
    response = client.client.get("/api")
    assert response.status_code == 200
    assert response.json() == "Hello from IFSGuid!"


@pytest.mark.asyncio
async def test_get_all_interactions(db):
    async with client.async_session() as db:
        try:
            await client.create_tables()
            interaction1 = models.Interaction(settings={"prompt": "something"})
            interaction2 = models.Interaction(settings={"prompt": "something else"})
            db.add(interaction1)
            db.add(interaction2)
            await db.commit()

            response = client.client.get("/api/interactions")
            assert response.status_code == 200
            assert len(response.json()) == 2
        finally:
            await client.drop_tables()


@pytest.mark.asyncio
async def test_create_interaction():
    async with client.async_session() as db:
        try:
            await client.create_tables()
            response = client.client.post(
                "/api/interactions",
                json={
                    "prompt": "something",
                },
            )
            assert response.status_code == 200
            assert response.json()["settings"] == {
                "prompt": "something",
                "model": "gpt-3.5-turbo",
                "role": "System",
            }
        finally:
            await client.drop_tables()
