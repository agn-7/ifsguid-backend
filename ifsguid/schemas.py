from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import List


class MessageCreate(BaseModel):
    role: str = "human"
    content: str

    class Config:
        from_attributes = True


class Message(MessageCreate):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class Settings(BaseModel):
    model_name: str = "GPT4"
    role: str = "System"
    prompt: str


class InteractionCreate(BaseModel):
    settings: Settings

    class config:
        from_attributes = True


class Interaction(InteractionCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime
    messages: List[Message] = []

    class Config:
        from_attributes = True
