from datetime import datetime

from ifsguid import crud, models, utils, schemas


### Unit Tests ###


def test_get_interactions(db):
    timestamp = utils.convert_timezone(datetime.now())
    interaction1 = models.Interaction(
        settings=dict(model_name="model1", role="role1", prompt="prompt1"),
        created_at=timestamp,
        updated_at=timestamp,
    )
    interaction2 = models.Interaction(
        settings=dict(model_name="model2", role="role2", prompt="prompt2"),
        created_at=timestamp,
        updated_at=timestamp,
    )
    db.add(interaction1)
    db.add(interaction2)
    db.commit()

    interactions = crud.get_interactions(db)
    assert len(interactions) == 2
    assert interactions[0].settings["model_name"] == "model1"
    assert interactions[1].settings["model_name"] == "model2"


