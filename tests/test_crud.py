import pytest

from ifsguid import crud, models, schemas
from . import client


### Unit Tests ###


@pytest.mark.asyncio
async def test_get_interactions(db):
    async for db in db:  # TODO
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


@pytest.mark.asyncio
async def test_get_interaction(db):
    async for db in db:  # TODO
        interaction = models.Interaction(
            settings=dict(model="model", role="role", prompt="prompt"),
        )
        db.add(interaction)
        await db.commit()

        retrieved_interaction = await crud.get_interaction(db, interaction.id)
        assert retrieved_interaction.id == interaction.id
        assert retrieved_interaction.settings["model"] == "model"
