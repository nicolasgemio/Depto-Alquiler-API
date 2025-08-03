from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, desc
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import uuid
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base, SEARCH_DEPARTMENT_TABLE, DEPARTMENT_CLASS, PARTICIPANT_REACTION_CLASS, PARTICIPANT_COMMENT_CLASS
from models.participant_reaction import ParticipantReaction
from models.participant_comment import ParticipantComment

class SearchDepartment(Base):
    __tablename__ = SEARCH_DEPARTMENT_TABLE

    search_department_id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    search_id = Column(ForeignKey("searches.search_id"))
    create_date = Column(DateTime)
    department_id = Column(ForeignKey("departments.department_id"))
    department = relationship(DEPARTMENT_CLASS, back_populates="search_links")
    participant_reactions: Mapped[list[ParticipantReaction]] = relationship(PARTICIPANT_REACTION_CLASS, cascade="all, delete-orphan", lazy="joined")
    participant_comments: Mapped[list[ParticipantComment]] = relationship(PARTICIPANT_COMMENT_CLASS, cascade="all, delete-orphan", lazy="joined", order_by=lambda: desc(ParticipantComment.create_date))
    is_removed = Column(Boolean, default=False)