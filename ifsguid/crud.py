from typing import List
from uuid import UUID

from sqlalchemy import delete, update
from sqlalchemy.orm import joinedload
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
    await db.refresh(interaction)

    return interaction


async def delete_interaction(db: AsyncSession, id: UUID) -> None:
    stmt = delete(models.Interaction).where(models.Interaction.id == id)
    result = await db.execute(stmt)

    if result.rowcount:
        await db.commit()
        return True

    return False


async def update_interaction(
    db: AsyncSession, id: UUID, settings: schemas.Settings
) -> models.Interaction:
    stmt = (
        update(models.Interaction)
        .where(models.Interaction.id == id)
        .values(settings=settings)
    )
    result = await db.execute(stmt)

    if result.rowcount:
        await db.commit()
        return True

    return None


async def get_messages(
    db: AsyncSession, interaction_id: UUID = None, page: int = None, per_page: int = 10
) -> List[models.Message]:
    stmt = select(models.Message)

    if interaction_id is not None:
        stmt = stmt.where(models.Message.interaction_id == interaction_id)

    if page is not None:
        stmt = stmt.offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(stmt)
    return result.scalars().all()


async def create_message(
    db: AsyncSession, messages: List[schemas.MessageCreate], interaction_id: UUID
) -> List[models.Message]:
    messages_db = []
    for msg in messages:
        message = models.Message(
            **msg.model_dump(),
            interaction_id=interaction_id,
        )
        db.add(message)
        messages_db.append(message)

    await db.commit()
    return messages_db
