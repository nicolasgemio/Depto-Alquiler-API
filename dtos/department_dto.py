from pydantic import BaseModel
from datetime import datetime
from dtos.participant_reaction_dto import ParticipantReactionDto
from uuid import UUID

class DepartmentDto(BaseModel):
    title: str | None = None
    department_id: UUID | None = None
    link: str
    address: str | None = None
    neighborhood: str | None = None
    photo_url: str | None = None
    price: int | None = None
    price_currency: str | None = None
    publication_date: datetime | None = None
    create_date: datetime | None = None
    search_links: list[ParticipantReactionDto] | None = None

    class Config:
        from_attributes = True