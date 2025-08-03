from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class ParticipantReactionDto(BaseModel):
    participant_reaction_id: UUID | None = None
    participant_id: UUID | None = None
    search_department_id: UUID | None = None
    create_date: datetime | None = None
    search_id: UUID | None = None
    reaction: str | None = None
    
    class Config:
        from_attributes = True