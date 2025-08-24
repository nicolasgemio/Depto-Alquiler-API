import pytz
from dtos.department_dto import DepartmentDto
from dtos.search_dto import SearchDto
from models.search import Search
from models.search_department import SearchDepartment
from models.search_participant import SearchParticipant
from models.department import Department
from database import SessionLocal
from sqlalchemy.orm import joinedload
from uuid import UUID
from dtos.search_participant_dto import SearchParticipantDto
from datetime import datetime, timezone

class SearchRepository:
    def __init__(self):
        pass

    def get_all(self) -> list[SearchDto]:
        with SessionLocal() as db:
            try:
                searches = (
                    db.query(Search)
                    .options(joinedload(Search.search_filters))
                    .all()
                )
                searches_dto = [SearchDto.model_validate(search) for search in searches]
                return searches_dto
            except Exception as e:
                db.rollback()
                print("Error al hacer commit:", e)
                raise

    def get_searches(self, user_id: str) -> list[SearchDto]:
        with SessionLocal() as db:
            try:
                searches = (
                    db.query(Search)
                    # filtra solo los Search que tengan al menos un SearchParticipant con user_id == user_id
                    .filter(Search.search_participants.any(user_id=user_id))
                    .options(joinedload(Search.search_participants))
                    .all()
                )
                searches_dto = [SearchDto.model_validate(search) for search in searches]
                return searches_dto
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

    def get_if_exists(self, search_id: str, department_code: str):
        with SessionLocal() as db:
            try:
                department = db.query(Department).filter(
                    Department.department_code == department_code
                department = db.query(Department).filter(
                    Department.department_code == department_code
                ).first()
                if not department:
                    return None, False
                department_id = department.department_id
                exists = db.query(SearchDepartment).filter(
                    SearchDepartment.search_id == search_id,
                    SearchDepartment.department_id == department_id
                ).first() is not None
                return department_id, exists
                print("Error al hacer commit:", e)
                raise

    def insert_search_department(self, search_id: str, department_id: str):
        with SessionLocal() as db:
            try:
                new_record = SearchDepartment(
                    search_id=search_id,
                    department_id=department_id,
                    create_date=datetime.now(timezone.utc),
                    is_removed=False
                )
                db.add(new_record)
                db.commit()
                db.refresh(new_record)
                return new_record
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

    def get_not_loaded(self, search_id: str, codes: list[str]) -> list[DepartmentDto]:
        """
        Devuelve DepartmentDto para los departments con department_code en 'codes' que NO están asociados al search_id.
        """
        with SessionLocal() as db:
            try:
                # 1. Traer todos los departamentos con esos códigos
                departments = db.query(Department).filter(Department.department_code.in_(codes)).all()
                department_id_map = {str(dept.department_id): dept for dept in departments}
                all_ids = list(department_id_map.keys())
                # 2. Traer los IDs ya cargados
                loaded = db.query(SearchDepartment.department_id).filter(
                    SearchDepartment.search_id == search_id,
                    SearchDepartment.department_id.in_(all_ids),
                    SearchDepartment.is_removed == False
                ).all()
                loaded_ids = {str(dep_id[0]) for dep_id in loaded}
                # 3. Filtrar los que NO están cargados
                not_loaded = [dept for did, dept in department_id_map.items() if did not in loaded_ids]
                # 4. Convertir a DTO
                results = [DepartmentDto.model_validate(dept) for dept in not_loaded]
                print(f"Departamentos no cargados encontrados: {len(results)} de {len(departments)} códigos")
                return results
            except Exception as ex:
                db.rollback()
                print(f"Excepción en get_not_loaded: search_id={search_id}, ex={ex}")
                raise