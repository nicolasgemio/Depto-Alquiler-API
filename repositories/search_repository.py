import pytz
from dtos.search_dto import SearchDto
from models.search import Search
from models.search_department import SearchDepartment
from models.search_participant import SearchParticipant
from database import SessionLocal
from sqlalchemy.orm import joinedload
from uuid import UUID
from dtos.search_participant_dto import SearchParticipantDto
from dtos.search_department_dto import SearchDepartmentDto

class SearchRepository:
    def __init__(self):
        pass

    def get_searches(self, user_id: str) -> SearchDto | None:
        with SessionLocal() as db:
            try:
                searches = (db.query(Search)
                            .filter(Search.user_id == user_id)
                            .options(joinedload(Search.search_participants))
                            .all())

                search_dto = [SearchDto.model_validate(search) for search in searches]
                return search_dto
            except Exception as e:
                db.rollback()
                print("Error al hacer commit:", e)
                raise
    
    def get_search_department(self, search_department_id: str) -> SearchDepartment | None:
        with SessionLocal() as db:
            try:
                search_department = db.query(SearchDepartment).filter(SearchDepartment.search_department_id == search_department_id).first()
                if not search_department:
                    return None
                return search_department
            except Exception as e:
                db.rollback()
                print("Error al hacer commit:", e)
                raise
    
    def get_search_participants(self, search_id: UUID) -> list[SearchParticipantDto]:
        with SessionLocal() as db:
            try:
                participants = (db.query(SearchParticipant)
                                .filter(SearchParticipant.search_id == search_id)
                                .all())

                participants_dto = [SearchParticipantDto.model_validate(participant) for participant in participants]
                return participants_dto
            except Exception as e:
                db.rollback()
                print("Error al hacer commit:", e)
                raise

    def get_local_time(self, date):
        utc_dt = date.replace(tzinfo=pytz.utc)

        local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
        local_dt = utc_dt.astimezone(local_tz)

        fecha_local = local_dt.strftime("%Y-%m-%d %H:%M:%S")

        return fecha_local