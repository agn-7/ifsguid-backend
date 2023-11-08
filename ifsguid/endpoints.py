from typing import List, Dict, Any, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, schemas, modules
from .database import SessionLocal

router = APIRouter()


def get_db() -> SessionLocal:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/", response_model=str)
async def get_root(db: Session = Depends(get_db)) -> str:
    return "Hello from IFSGuid!"


@router.get("/interactions", response_model=List[schemas.Interaction])
async def get_all_interactions(
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    db: Session = Depends(get_db),
) -> List[schemas.Interaction]:
    return [
        schemas.Interaction.model_validate(interaction)
        for interaction in crud.get_interactions(db=db, page=page, per_page=per_page)
    ]


@router.get(
    "/interactions/{id}", response_model=schemas.Interaction, include_in_schema=False
)
async def get_interactions(
    id: UUID, db: Session = Depends(get_db)
) -> schemas.Interaction:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="NotImplementedError"
    )


@router.post("/interactions", response_model=schemas.Interaction)
async def create_interactions(
    settings: schemas.Settings, db: Session = Depends(get_db)
) -> schemas.Interaction:
    return schemas.Interaction.model_validate(
        crud.create_interaction(db=db, settings=settings)
    )


@router.delete("/interactions", response_model=Dict[str, Any], include_in_schema=False)
async def delete_interaction(id: UUID, db: Session = Depends(get_db)) -> None:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="NotImplementedError"
    )


@router.put(
    "/interactions/{id}", response_model=schemas.Interaction, include_in_schema=False
)
async def update_interaction(
    id: UUID, settings: schemas.Settings, db: Session = Depends(get_db)
) -> schemas.Interaction:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="NotImplementedError"
    )


