from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from . import models, schemas, utils


def get_interactions(
        db: Session, page: int = None, per_page: int = 10
    ) -> List[models.Interaction]:
    query = db.query(models.Interaction)

    if page is not None:
        query = query.offset((page - 1) * per_page).limit(per_page)

    return query.all()


def get_interaction(db: Session, id: UUID) -> models.Interaction:
    return db.query(models.Interaction).filter(models.Interaction.id == id).first()


def create_interaction(db: Session, settings: schemas.Settings) -> models.Interaction:
    timestamp = utils.convert_timezone(datetime.now())
    interaction = models.Interaction(
        settings=settings.model_dump(), created_at=timestamp, updated_at=timestamp,
    )
    db.add(interaction)
    db.commit()
    return interaction


def delete_interaction(db: Session, id: UUID) -> None:
    interaction = db.query(
        models.Interaction
    ).filter(models.Interaction.id == id).first()

    if interaction is not None:
        db.delete(interaction)
        db.commit()
        return True

    return False


def update_interaction(
        db: Session, id: UUID, settings: schemas.Settings
    ) -> models.Interaction:
    interaction: models.Interaction = db.query(
        models.Interaction
    ).filter(models.Interaction.id == id).first()

    if interaction is not None:
        interaction.settings = settings
        interaction.updated_at = utils.convert_timezone(datetime.now())
        db.commit()
        return interaction

    return None

