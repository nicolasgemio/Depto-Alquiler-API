from datetime import datetime
from pydantic import BaseModel
from dtos.department_dto import DepartmentDto
from dtos.participant_reaction_dto import ParticipantReactionDto
from uuid import UUID
from dtos.user_dto import UserDto

class SearchParticipantDto(BaseModel):
    search_id: UUID | None = None
    user_id: UUID | None = None
    create_date: datetime | None = None
    user: UserDto | None = None

    class Config:
        from_attributes = True