from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import uuid
from sqlalchemy.orm import relationship
from database import Base, SEARCH_FILTER_TABLE

class SearchFilter(Base):
    __tablename__ = SEARCH_FILTER_TABLE

    search_filter_id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    name = Column(String(10))
    filter_value = Column(String)
    search_id = Column(ForeignKey("searches.search_id"))
    search = relationship("Search", back_populates="search_filters")
