from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import uuid
from database import Base, SEARCH_DEPARTMENT_CLASS, DEPARTMENT_TABLE
from sqlalchemy.orm import relationship

class Department(Base):
    __tablename__ = DEPARTMENT_TABLE

    department_id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    link = Column(String)
    address = Column(String)
    neighborhood = Column(String)
    photo_url = Column(String)
    price = Column(Integer)
    price_currency = Column(String)
    publication_date = Column(DateTime)
    title = Column(String)
    create_date = Column(DateTime)
    search_links = relationship(SEARCH_DEPARTMENT_CLASS, back_populates="department")
