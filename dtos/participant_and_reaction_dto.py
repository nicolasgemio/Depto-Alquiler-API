from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class ParticipantAndReactionDto(BaseModel):
    participant_id: UUID | None = None
    create_date: datetime | None = None
    reaction: str | None = None