from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import uuid
from sqlalchemy.orm import relationship
from database import Base, SEARCH_PARTICIPANT_TABLE, PARTICIPANT_COMMENT_CLASS, USER_CLASS

class SearchParticipant(Base):
    __tablename__ = SEARCH_PARTICIPANT_TABLE

    search_id = Column(ForeignKey("searches.search_id"), primary_key=True)
    user_id = Column(ForeignKey("users.user_id"), primary_key=True)
    create_date = Column(DateTime)
    search_links = relationship(PARTICIPANT_COMMENT_CLASS, back_populates="participant")
    user = relationship(USER_CLASS, back_populates="participant_user")


