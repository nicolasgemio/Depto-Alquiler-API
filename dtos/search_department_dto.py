from datetime import datetime
from pydantic import BaseModel, Field
from dtos.department_dto import DepartmentDto
from dtos.participant_and_reaction_dto import ParticipantAndReactionDto
from dtos.participant_reaction_dto import ParticipantReactionDto
from dtos.participant_comment_dto import ParticipantCommentDto
from uuid import UUID

class SearchDepartmentDto(BaseModel):
    search_department_id: UUID | None = None
    search_id: UUID | None = None
    create_date: datetime | None = None
    department_id: UUID | None = None
    department: DepartmentDto | None = None
    participant_reactions: list[ParticipantReactionDto] = Field(default_factory=list)
    participant_comments: list[ParticipantCommentDto] = Field(default_factory=list)
    reactions: list[ParticipantAndReactionDto] = Field(default_factory=list)
    is_removed: bool = False
    color: str | None = None

    class Config:
        from_attributes = True