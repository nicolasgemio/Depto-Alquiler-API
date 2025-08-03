from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, ForeignKeyConstraint
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import uuid
from sqlalchemy.orm import relationship
from database import Base, PARTICIPANT_COMMENT_TABLE, SEARCH_PARTICIPANT_CLASS

class ParticipantComment(Base):
    __tablename__ = PARTICIPANT_COMMENT_TABLE

    participant_comment_id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    participant_id = Column(UNIQUEIDENTIFIER)
    search_department_id = Column(ForeignKey("search_departments.search_department_id"))
    create_date = Column(DateTime)
    search_id = Column(UNIQUEIDENTIFIER)
    comment = Column(String(100))
    participant = relationship(SEARCH_PARTICIPANT_CLASS, back_populates="search_links")

    #Fore
    __table_args__ = (
        ForeignKeyConstraint(
            ['search_id', 'participant_id'],
            ['search_participants.search_id', 'search_participants.user_id']
        ),
    )