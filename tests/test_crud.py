import pytest

from ifsguid import crud, models, schemas
from . import client


### Unit Tests ###


@pytest.mark.asyncio
async def test_get_interactions(db):
    async with client.async_session() as db:
        try:
            await client.create_tables()
            interaction1 = models.Interaction(
                settings=dict(model="model1", role="role1", prompt="prompt1"),
            )
            interaction2 = models.Interaction(
                settings=dict(model="model2", role="role2", prompt="prompt2"),
            )
            db.add(interaction1)
            db.add(interaction2)
            await db.commit()

            interactions = await crud.get_interactions(db)
            assert len(interactions) == 2
            assert interactions[0].settings["model"] == "model1"
            assert interactions[1].settings["model"] == "model2"
        finally:
            await client.drop_tables()


@pytest.mark.asyncio
async def test_get_interaction(db):
    async with client.async_session() as db:
        try:
            await client.create_tables()
            interaction = models.Interaction(
                settings=dict(model="model", role="role", prompt="prompt"),
            )
            db.add(interaction)
            await db.commit()

            retrieved_interaction = await crud.get_interaction(db, interaction.id)
            assert retrieved_interaction.id == interaction.id
            assert retrieved_interaction.settings["model"] == "model"
        finally:
            await client.drop_tables()
