from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class UserDto(BaseModel):
    user_id: UUID | None = None
    google_id: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    email: str | None = None

    class Config:
        from_attributes = True