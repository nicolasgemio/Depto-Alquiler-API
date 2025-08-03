from datetime import datetime
from pydantic import BaseModel
from dtos.search_participant_dto import SearchParticipantDto
from uuid import UUID

class SearchDto(BaseModel):
    search_id: UUID | None = None
    title: str
    user_id: str
    create_date: datetime | None = None
    search_participants: list[SearchParticipantDto] | None = None

    class Config:
        from_attributes = True