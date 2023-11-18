from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import List, Literal


class MessageCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    role: Literal["human", "ai"] = "human"
    content: str


class Message(MessageCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime


class Settings(BaseModel):
    model_name: Literal["GPT4", "GPT3"] = "GPT3"
    role: Literal["System"] = "System"
    prompt: str


class InteractionCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    settings: Settings


class Interaction(InteractionCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    messages: List[Message] = []
