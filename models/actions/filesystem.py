from pydantic import BaseModel, Field


class CreateFolderPayload(BaseModel):
    path: str = Field(..., min_length=1)
