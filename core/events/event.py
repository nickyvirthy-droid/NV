from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from core.events.types import EventType


class Event(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: EventType
    source: str
    payload: dict = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
