from ifsguid import models
from .client import client


### Integration Tests ###


def test_get_root():
    response = client.get("/api")
    assert response.status_code == 200
    assert response.json() == "Hello from IFSGuid!"


def test_get_all_interactions(db):
    interaction1 = models.Interaction(settings={"prompt": "something"})
    interaction2 = models.Interaction(settings={"prompt": "something else"})
    db.add(interaction1)
    db.add(interaction2)
    db.commit()

    response = client.get("/api/interactions")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_create_interaction():
    response = client.post(
        "/api/interactions",
        json={
            "prompt": "something",
        },
    )
    assert response.status_code == 200
    assert response.json()["settings"] == {
        "prompt": "something",
        "model_name": "GPT3",
        "role": "System",
    }
