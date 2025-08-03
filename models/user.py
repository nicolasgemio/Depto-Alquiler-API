from sqlalchemy import Column, String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import uuid
from database import Base, USER_TABLE, SEARCH_PARTICIPANT_CLASS
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = USER_TABLE

    user_id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    google_id = Column(String)
    given_name = Column(String)
    family_name = Column(String)
    email = Column(String)
    participant_user = relationship(SEARCH_PARTICIPANT_CLASS, back_populates="user")