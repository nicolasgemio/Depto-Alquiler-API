from dtos.search_department_dto import SearchDepartmentDto
from datetime import datetime, timezone
from database import SessionLocal
from models.department import Department
from models.search_department import SearchDepartment
from models.participant_reaction import ParticipantReaction
from models.participant_comment import ParticipantComment
from sqlalchemy.orm import joinedload
from database import DEPARTMENT_TABLE

class DepartmentRepository:
    def __init__(self):
        pass

    def get_by_search_department_id(self, search_department_id: str) -> SearchDepartmentDto | None:
        """
        Obtiene un SearchDepartmentDto a partir de un search_department_id.
        Args:
            search_department_id (str): ID del SearchDepartment a buscar.
        Returns:
            SearchDepartmentDto | None: DTO del departamento encontrado o None si no existe.
        """
        with SessionLocal() as db:
            try:
                search_department = (db.query(SearchDepartment)
                            .filter(SearchDepartment.search_department_id == search_department_id)
                            .options(joinedload(SearchDepartment.participant_reactions))
                            .options(joinedload(SearchDepartment.participant_comments))
                            .first())
                        
                search_department_dto = SearchDepartmentDto.model_validate(search_department) 

                return search_department_dto
            except Exception as e:
                db.rollback()
                print("Error al hacer commit:", e)
                raise


    def get_by_search_id(self, search_id: str, user_id: str) -> list[SearchDepartment]:
        """
        Obtiene una lista de SearchDepartmentDto asociados a un search_id y los ordena según las reacciones del usuario.
        Args:
            search_id (str): ID de la búsqueda.
            user_id (str): ID del usuario para ordenar según sus reacciones.
        Returns:
            list[SearchDepartmentDto]: Lista ordenada de DTOs de departamentos encontrados.
        """
        db = SessionLocal
        # 2) defino función para computar claves de orden
        def sort_key(sd: SearchDepartment):
            reactions = sd.participant_reactions
            total_fav = sum(1 for r in reactions if r.reaction == 'favorite')
            total_rej = sum(1 for r in reactions if r.reaction == 'reject')
            user_fav = any(r for r in reactions if r.participant_id == user_id and r.reaction == 'favorite')
            user_rej = any(r for r in reactions if r.participant_id == user_id and r.reaction == 'reject')
            # clave:
            # 1er campo: user_rej False(0) → True(1)  => los con user_rej van al final
            # 2º campo: user_fav False(0) → True(1)  => los con favorito del user al final de este bloque
            # 3er:   -total_fav  (más fav → antes)
            # 4º:    total_rej  (menos rechazos → antes)
            # 5º:    fecha creación ascendente
            return (
                int(user_rej),
                int(user_fav),
                -total_fav,
                total_rej,
                sd.department.create_date
            )
        
        with SessionLocal() as db:
            # 1) traigo todo como antes
            results = (
                db.query(SearchDepartment)
                  .join(Department)
                  .filter(
                     SearchDepartment.search_id == search_id,
                     SearchDepartment.is_removed == False
                  )
                  .options(joinedload(SearchDepartment.participant_reactions))
                  .options(joinedload(SearchDepartment.participant_comments))
                  .all()
            )
            # 3) retorno la lista ordenada
            ordered = sorted(results, key=sort_key)
            search_departments_dto = [SearchDepartmentDto.model_validate(department) for department in ordered]

            return search_departments_dto
    
    def react_department(self, new_reaction: ParticipantReaction) -> ParticipantReaction:
        """
        Inserta o actualiza una reacción de un participante sobre un departamento.
        Args:
            new_reaction (ParticipantReaction): Objeto de reacción a insertar o actualizar.
        Returns:
            ParticipantReaction: Objeto de reacción insertado o actualizado.
        """
        with SessionLocal() as db:
            try:
                existing = db.query(ParticipantReaction).filter_by(
                    participant_id=new_reaction.participant_id,
                    search_department_id=new_reaction.search_department_id,
                    search_id=new_reaction.search_id
                ).first()

                if existing:
                    # Ya existe → actualizar solo el campo reaction
                    existing.reaction = new_reaction.reaction
                    existing.create_date = datetime.now(timezone.utc)
                    db.commit()
                    db.refresh(existing)
                    return existing
                else:
                    # No existe → insertar nuevo
                    db.add(new_reaction)
                    db.commit()
                    db.refresh(new_reaction)
                    return new_reaction

            except Exception as e:
                db.rollback()
                print("Error al hacer commit:", e)
                raise

    def remove_department(self, search_department: SearchDepartment, new_reaction: ParticipantReaction) -> ParticipantReaction:
        """
        Marca un departamento como removido y registra la reacción correspondiente del participante.
        Args:
            search_department (SearchDepartment): Departamento a marcar como removido.
            new_reaction (ParticipantReaction): Reacción a registrar.
        Returns:
            ParticipantReaction: Objeto de reacción insertado o actualizado.
        """
        with SessionLocal as db:
            try:

                existing = db.query(SearchDepartment).filter_by(
                    search_department_id = search_department.search_department_id,
                ).first()

                if existing:
                    existing.is_removed = True

                existing = db.query(ParticipantReaction).filter_by(
                    participant_id=new_reaction.participant_id,
                    search_department_id=new_reaction.search_department_id,
                    search_id=new_reaction.search_id
                ).first()

                if existing:
                    existing.reaction = new_reaction.reaction
                    existing.create_date = datetime.now(timezone.utc)
                    db.commit()
                    db.refresh(existing)
                    return existing
                else:
                    db.add(new_reaction)
                    db.commit()
                    db.refresh(new_reaction)
                    return new_reaction
            except Exception as e:
                db.rollback()
                print(f"Error al remover el departamento: {e}")
                raise

            
    def comment_department(self, new_commentary: ParticipantComment):
        """
        Inserta un nuevo comentario de participante sobre un departamento.
        Args:
            new_commentary (ParticipantComment): Comentario a insertar.
        Returns:
            ParticipantComment: Objeto de comentario insertado.
        """
        with SessionLocal() as db:
            try:
                db.add(new_commentary)
                db.commit()
                db.refresh(new_commentary)
                return new_commentary
            except Exception as e:
                db.rollback()
                print(f"Error al comentar el departamento: {e}")
                raise

    def insert_department(self, department: Department) -> Department:
        """
        Inserta un nuevo departamento en la base de datos.
        """
        with SessionLocal() as db:
            try:
                db.add(department)
                db.commit()
                db.refresh(department)
                return department
            except Exception as e:
                db.rollback()
                print(f"Error al insertar el departamento: {e}")
                raise

    def exists_department(self, **kwargs) -> bool:
        """
        Verifica si existe un departamento según los campos clave pasados como kwargs.
        Ejemplo: exists_department(external_id='1234')
        """
        with SessionLocal() as db:
            query = db.query(Department).filter_by(**kwargs)
            exists = db.query(query.exists()).scalar()
            return bool(exists)

    def get_nonexistent_department_codes(self, codes: list[str]) -> list[str]:
        """
        Dada una lista de department_code, retorna solo los que NO existen en la base de datos.
        Args:
            codes (list[str]): Lista de códigos a verificar.
        Returns:
            list[str]: Códigos que no existen en la base de datos.
        """
        with SessionLocal() as db:
            existing = db.query(Department.department_code).filter(Department.department_code.in_(codes)).all()
            existing_codes = set(row[0] for row in existing)
            return [code for code in codes if code not in existing_codes]
