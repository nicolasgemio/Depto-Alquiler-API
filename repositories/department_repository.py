from dtos.search_department_dto import SearchDepartmentDto
from datetime import datetime, timezone
from firebase_admin import credentials, firestore
from database import SessionLocal
from models.department import Department
from models.search_department import SearchDepartment
from models.participant_reaction import ParticipantReaction
from models.participant_comment import ParticipantComment
from sqlalchemy.orm import joinedload
from database import DEPARTMENT_TABLE
from enumerables.reaction_type_enum import ReactionTypeEnum

class DepartmentRepository:
    def __init__(self):
        self.db = firestore.client()
        self.collection = self.db.collection(DEPARTMENT_TABLE)

    def get_by_search_department_id(self, search_department_id: str) -> SearchDepartment | None:
        self.db = SessionLocal()
        search_department = (self.db.query(SearchDepartment)
                    .filter(SearchDepartment.search_department_id == search_department_id)
                    .options(joinedload(SearchDepartment.participant_reactions))
                    .options(joinedload(SearchDepartment.participant_comments))
                    .first())
        
        return search_department
    
    def get_all(self) -> list[SearchDepartmentDto]:
        return [
            SearchDepartmentDto(id=doc.id, **doc.to_dict())
            for doc in self.collection.stream()
        ]

    def get_by_search_id(self, search_id: str) -> list[SearchDepartment]:
        db = SessionLocal()
        results = (db.query(SearchDepartment)
                    .join(Department)
                    .filter(SearchDepartment.search_id == search_id, SearchDepartment.is_removed == False)
                    .options(joinedload(SearchDepartment.participant_reactions))
                    .options(joinedload(SearchDepartment.participant_comments))
                    .all())
        
        return results
    
    def react_department(self, new_reaction: ParticipantReaction) -> ParticipantReaction:
        db = SessionLocal()
    
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

    def remove_department(self, search_department: SearchDepartment, new_reaction: ParticipantReaction) -> list[ParticipantReaction]:
        db = SessionLocal()
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
        db = SessionLocal()
        try:
            db.add(new_commentary)
            db.commit()
            db.refresh(new_commentary)
            return new_commentary
        except Exception as e:
            db.rollback()
            print(f"Error al comentar el departamento: {e}")
            raise

