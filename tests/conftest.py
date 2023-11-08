import pytest

from ifsguid import models
from .client import override_get_db, engine


@pytest.fixture
def db():
    try:
        yield from override_get_db()
    finally:
        models.Base.metadata.drop_all(bind=engine)
