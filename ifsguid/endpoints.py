from typing import List, Dict, Any, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from g4f import ModelUtils

from . import crud, schemas, modules
from .database import async_session, AsyncSession

router = APIRouter()


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


@router.get("/", response_model=str)
async def get_root(db: AsyncSession = Depends(get_db)) -> str:
    return "Hello from IFSGuid!"


@router.get("/interactions", response_model=List[schemas.Interaction])
async def get_all_interactions(
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
) -> List[schemas.Interaction]:
    interactions = await crud.get_interactions(db=db, page=page, per_page=per_page)

    return [
        schemas.Interaction.model_validate(interaction) for interaction in interactions
    ]


@router.get(
    "/interactions/{id}", response_model=schemas.Interaction, include_in_schema=False
)
async def get_interactions(
    id: UUID, db: AsyncSession = Depends(get_db)
) -> schemas.Interaction:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="NotImplementedError"
    )


@router.post("/interactions", response_model=schemas.Interaction)
async def create_interactions(
    prompt: schemas.Prompt,
    chat_model: schemas.ChatModel = Depends(),
    db: AsyncSession = Depends(get_db),
) -> schemas.Interaction:
    settings = schemas.Settings(
        model=chat_model.model, prompt=prompt.prompt, role=prompt.role
    )
    interaction = await crud.create_interaction(db=db, settings=settings)

    return schemas.Interaction.model_validate(interaction)


@router.delete("/interactions", response_model=Dict[str, Any], include_in_schema=False)
async def delete_interaction(id: UUID, db: AsyncSession = Depends(get_db)) -> None:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="NotImplementedError"
    )


@router.put(
    "/interactions/{id}", response_model=schemas.Interaction, include_in_schema=False
)
async def update_interaction(
    id: UUID, settings: schemas.Settings, db: AsyncSession = Depends(get_db)
) -> schemas.Interaction:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="NotImplementedError"
    )


@router.get(
    "/interactions/{interaction_id}/messages", response_model=List[schemas.Message]
)
async def get_all_message_in_interaction(
    interaction_id: UUID,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
) -> List[schemas.Message]:
    interaction = crud.get_interaction(db=db, id=str(interaction_id))

    if not interaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Interaction not found"
        )

    return [
        schemas.Message.model_validate(message)
        for message in crud.get_messages(
            db=db, interaction_id=str(interaction_id), page=page, per_page=per_page
        )
    ]


@router.post(
    "/interactions/{interactions_id}/messages", response_model=List[schemas.Message]
)
async def create_message(
    interaction_id: UUID,
    message: schemas.MessageCreate,
    db: AsyncSession = Depends(get_db),
) -> schemas.Message:
    interaction = await crud.get_interaction(db=db, id=str(interaction_id))

    if not interaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Interaction not found"
        )

    interaction = schemas.Interaction.model_validate(interaction)

    messages = []
    if message.role == "human":
        ai_content = await modules.generate_ai_response(
            content=message.content,
            model=ModelUtils.convert[interaction.settings.model],
        )
        ai_message = schemas.MessageCreate(role="ai", content=ai_content)

        messages.append(message)
        messages.append(ai_message)

    messages = await crud.create_message(
        db=db, messages=messages, interaction_id=str(interaction_id)
    )
    return [schemas.Message.model_validate(message) for message in messages]
