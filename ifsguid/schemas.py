from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import List, Literal

from g4f import _all_models


class MessageCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    role: Literal["human", "ai"] = "human"
    content: str


class Message(MessageCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime


class ChatModel(BaseModel):
    model: Literal[tuple(_all_models)] = "gpt-3.5-turbo"


class Prompt(BaseModel):
    role: Literal["system"] = "system"
    prompt: str


class Settings(ChatModel, Prompt):
    pass


class InteractionCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    settings: Settings


class Interaction(InteractionCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    messages: List[Message] = []
