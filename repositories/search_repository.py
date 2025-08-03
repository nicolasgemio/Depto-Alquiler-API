import pytz
from datetime import datetime
from firebase_admin import credentials, firestore
from dtos.search_dto import SearchDto
from models.search import Search
from models.search_department import SearchDepartment
from models.search_participant import SearchParticipant
from database import SessionLocal
from sqlalchemy.orm import joinedload
from uuid import UUID

class SearchRepository:
    def __init__(self):
        self.db = firestore.client()
    
        self.collection = self.db.collection("searches")

    def get_searches(self, user_id: str) -> Search | None:
        db = SessionLocal()
        searches = (db.query(Search)
                    .filter(Search.user_id == user_id)
                    .options(joinedload(Search.search_participants))
                    .all())
        
        return searches
    
    def get_search_department(self, search_department_id: str) -> SearchDepartment | None:
        db = SessionLocal()
        search_department = db.query(SearchDepartment).filter(SearchDepartment.search_department_id == search_department_id).first()
        if not search_department:
            return None
        return search_department
    
    def get_search_participants(self, search_id: UUID) -> list[SearchParticipant]:
        db = SessionLocal()
        participants = (db.query(SearchParticipant)
                        .filter(SearchParticipant.search_id == search_id)
                        .all())
        
        return participants

    def get_local_time(self, date):
        utc_dt = date.replace(tzinfo=pytz.utc)

        local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
        local_dt = utc_dt.astimezone(local_tz)

        fecha_local = local_dt.strftime("%Y-%m-%d %H:%M:%S")

        return fecha_local