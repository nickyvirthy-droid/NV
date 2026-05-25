from typing import Any
from pydantic import BaseModel, Field


class ActionProtocol(BaseModel):
    action: str = Field(..., min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)
