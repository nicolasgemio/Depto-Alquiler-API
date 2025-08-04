from datetime import datetime
from dtos.search_participant_dto import SearchParticipantDto
from uuid import UUID
from pydantic import BaseModel, Field


class SearchDto(BaseModel):
    search_id: UUID | None = None
    title: str
    user_id: UUID | None = None
    create_date: datetime | None = None
    search_participants: list[SearchParticipantDto] = Field(default_factory=list)

    class Config:
        from_attributes = True