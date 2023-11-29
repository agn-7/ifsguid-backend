from typing import List
from uuid import UUID

from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_interactions(
    db: AsyncSession, page: int = None, per_page: int = 10
) -> List[models.Interaction]:
    stmt = select(models.Interaction).options(joinedload(models.Interaction.messages))

    if page is not None:
        stmt = stmt.offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(stmt)
    return result.scalars().unique().all()


async def get_interaction(db: AsyncSession, id: UUID) -> models.Interaction:
    stmt = select(models.Interaction).where(models.Interaction.id == id)
    result = await db.execute(stmt)
    return result.scalar()


async def create_interaction(
    db: AsyncSession, settings: schemas.Settings
) -> models.Interaction:
    interaction = models.Interaction(
        settings=settings.model_dump(),
    )
    db.add(interaction)
    await db.commit()
    result = await db.execute(
        select(models.Interaction)
        .options(joinedload(models.Interaction.messages))
        .where(models.Interaction.id == interaction.id)
    )
    interaction = result.scalars().unique().one()

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
