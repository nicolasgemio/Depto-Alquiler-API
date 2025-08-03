from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, ForeignKeyConstraint
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import uuid
from sqlalchemy.orm import relationship
from database import Base, PARTICIPANT_REACTION_TABLE

class ParticipantReaction(Base):
    __tablename__ = PARTICIPANT_REACTION_TABLE

    participant_reaction_id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    participant_id = Column(UNIQUEIDENTIFIER)
    search_department_id = Column(ForeignKey("search_departments.search_department_id"))
    create_date = Column(DateTime)
    search_id = Column(UNIQUEIDENTIFIER)
    reaction = Column(String(30))
    
    #Fore
    __table_args__ = (
        ForeignKeyConstraint(
            ['search_id', 'participant_id'],
            ['search_participants.search_id', 'search_participants.user_id']
        ),
    )