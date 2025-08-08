import pytz
from repositories.search_repository import SearchRepository
from models.search_department import SearchDepartment
from uuid import UUID
from dtos.search_participant_dto import SearchParticipantDto
from dtos.search_dto import SearchDto

class SearchService:
    def __init__(self, repository: SearchRepository):
        self.repository = repository

    def get_all(self) -> list[SearchDto]:
        searches = self.repository.get_all()
        return searches

    def get_searches(self, user_id) -> list[SearchDto]:
        if user_id is None or user_id == UUID(int=0):
            return []
        
        searches = self.repository.get_searches(user_id)
        return searches
    
    def get_search_department(self, search_department_id: str) -> SearchDepartment | None:
        return self.repository.get_search_department(search_department_id)
    
    def get_search_participants(self, search_id: UUID) -> list[SearchParticipantDto]:
        return self.repository.get_search_participants(search_id)
    
    def get_local_time(create_date):
        utc_dt = create_date.replace(tzinfo=pytz.utc)

        local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
        local_dt = utc_dt.astimezone(local_tz)
        fecha_local = local_dt.strftime("%Y-%m-%d %H:%M:%S")

        return fecha_local
