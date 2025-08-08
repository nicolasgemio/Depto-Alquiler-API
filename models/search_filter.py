from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import uuid
from sqlalchemy.orm import relationship
from database import Base, SEARCH_FILTER_TABLE

class SearchFilter(Base):
    __tablename__ = SEARCH_FILTER_TABLE

    name = Column(String(10))
    search_filter_id = Column(UNIQUEIDENTIFIER)
    filter_value = Column(String)
    search_id = Column(ForeignKey("searches.search_id"), primary_key=True)
