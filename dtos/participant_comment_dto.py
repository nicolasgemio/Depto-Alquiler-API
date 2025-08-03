from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from dtos.search_participant_dto import SearchParticipantDto

class ParticipantCommentDto(BaseModel):
    participant_comment_id: UUID | None = None
    participant_id: UUID | None = None
    search_department_id: UUID | None = None
    create_date: datetime | None = None
    search_id: UUID | None = None
    comment: str | None = None
    participant: SearchParticipantDto | None = None
    
    class Config:
        from_attributes = True