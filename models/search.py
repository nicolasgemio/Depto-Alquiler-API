from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import uuid
from sqlalchemy.orm import relationship
from database import Base, SEARCH_TABLE, SEARCH_PARTICIPANT_CLASS

class Search(Base):
    __tablename__ = SEARCH_TABLE

    search_id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    title = Column(String)
    user_id = Column(UNIQUEIDENTIFIER, default=lambda: str(uuid.uuid4))
    create_date = Column(DateTime)
    search_participants = relationship(SEARCH_PARTICIPANT_CLASS, cascade="all, delete-orphan", lazy="joined")