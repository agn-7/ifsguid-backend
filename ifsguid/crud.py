from typing import List
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from . import models, schemas, utils


def get_interactions(
    db: Session, page: int = None, per_page: int = 10
) -> List[models.Interaction]:
    query = db.query(models.Interaction).options(
        joinedload(models.Interaction.messages)
    )

    if page is not None:
        query = query.offset((page - 1) * per_page).limit(per_page)

    return query.all()


def get_interaction(db: Session, id: UUID) -> models.Interaction:
    return db.query(models.Interaction).filter(models.Interaction.id == id).first()


def create_interaction(db: Session, settings: schemas.Settings) -> models.Interaction:
    interaction = models.Interaction(
        settings=settings.model_dump(),
    )
    db.add(interaction)
    db.commit()
    return interaction


def delete_interaction(db: Session, id: UUID) -> None:
    interaction = (
        db.query(models.Interaction).filter(models.Interaction.id == id).first()
    )

    if interaction is not None:
        db.delete(interaction)
        db.commit()
        return True

    return False


def update_interaction(
    db: Session, id: UUID, settings: schemas.Settings
) -> models.Interaction:
    interaction: models.Interaction = (
        db.query(models.Interaction).filter(models.Interaction.id == id).first()
    )

    if interaction is not None:
        interaction.settings = settings
        db.commit()
        return interaction

    return None


def get_messages(
    db: Session, interaction_id: UUID = None, page: int = None, per_page: int = 10
) -> List[models.Message]:
    query = db.query(models.Message)

    if interaction_id is not None:
        query = query.filter(models.Message.interaction_id == interaction_id)

    if page is not None:
        query = query.offset((page - 1) * per_page).limit(per_page)

    return query.all()


def create_message(
    db: Session, messages: List[schemas.MessageCreate], interaction_id: UUID
) -> List[models.Message]:
    messages_db = []
    for msg in messages:
        message = models.Message(
            **msg.model_dump(),
            interaction_id=interaction_id,
        )
        db.add(message)
        messages_db.append(message)

    db.commit()
    return messages_db
