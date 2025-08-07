from repositories.department_repository import DepartmentRepository
from models.participant_reaction import ParticipantReaction
from models.participant_comment import ParticipantComment
from services.user_service import UserService
from services.search_service import SearchService
from uuid import UUID
import uuid
from datetime import datetime, timezone
from dtos.search_department_dto import SearchDepartmentDto
from dtos.participant_and_reaction_dto import ParticipantAndReactionDto
from dtos.participant_reaction_dto import ParticipantReactionDto
from enumerables.reaction_type_enum import ReactionTypeEnum
from models.department import Department


class DepartmentService:
    def __init__(self, repository: DepartmentRepository, user_service: UserService, search_service: SearchService):
        self.repository = repository
        self.user_service = user_service
        self.search_service = search_service


    def get_departments(self, search_id, user_id) -> list[SearchDepartmentDto]:
        if search_id is None or search_id == UUID(int=0):
            return []
        
        participants = self.search_service.get_search_participants(search_id)
        search_departments_dto = self.repository.get_by_search_id(search_id, user_id)

        for department in search_departments_dto:
            for participant in participants:
                reaction = next(
                    (r for r in department.participant_reactions if r.participant_id == participant.user_id),
                    None
                )

                if reaction:
                    department.reactions.append(
                        ParticipantAndReactionDto(
                            participant_id=participant.user_id,
                            reaction=reaction.reaction,
                            create_date=reaction.create_date
                        )
                    )
                else:
                    department.reactions.append(
                        ParticipantAndReactionDto(
                            participant_id=participant.user_id,
                            reaction=None,
                            create_date=None
                        )
                    )

        return search_departments_dto
    
    def react_department(self, search_department_id: str, google_id: str, reaction_type: str) -> ParticipantReaction:
        user = self.user_service.get_user(google_id)
        search_department = self.search_service.get_search_department(search_department_id)

        new_reaction = ParticipantReaction(
            participant_reaction_id = uuid.uuid4(),
            participant_id = user.user_id,
            search_department_id = search_department_id,
            create_date = datetime.now(timezone.utc),
            search_id = search_department.search_id,
            reaction=reaction_type
        )
        
        return self.repository.react_department(new_reaction)
    
    def remove_department(self, search_department_id: str,  google_id: str) -> ParticipantReaction:
        user = self.user_service.get_user(google_id)
        search_department = self.search_service.get_search_department(search_department_id)

        new_reaction = ParticipantReaction(
            participant_reaction_id = uuid.uuid4(),
            participant_id = user.user_id,
            search_department_id = search_department_id,
            create_date = datetime.now(timezone.utc),
            search_id = search_department.search_id,
            reaction=ReactionTypeEnum.REJECT
        )

        return self.repository.remove_department(search_department, new_reaction)

    def comment_department(self, search_department_id: str, google_id: str, commentary: str):
        user = self.user_service.get_user(google_id)
        search_department = self.search_service.get_search_department(search_department_id)

        new_commentary = ParticipantComment(
                participant_comment_id =uuid.uuid4(),
                participant_id = user.user_id,
                search_department_id = search_department_id,
                create_date = datetime.now(timezone.utc),
                search_id = search_department.search_id,
                comment = commentary
        )

        return self.repository.comment_department(new_commentary)


    def get_department_by_id(self, search_department_id) -> ParticipantReactionDto:
        if search_department_id is None or search_department_id == UUID(int=0):
            return []

        search_department_dto =self.repository.get_by_search_department_id(search_department_id)
        participants = self.search_service.get_search_participants(search_department_dto.search_id)

        for participant in participants:
            reaction = next(
                (r for r in search_department_dto.participant_reactions if r.participant_id == participant.user_id),
                None
            )

            if reaction:
                search_department_dto.reactions.append(
                    ParticipantAndReactionDto(
                        participant_id=participant.user_id,
                        reaction=reaction.reaction,
                        create_date=reaction.create_date
                    )
                )
            else:
                search_department_dto.reactions.append(
                    ParticipantAndReactionDto(
                        participant_id=participant.user_id,
                        reaction=None,
                        create_date=None
                    )
                )

        return search_department_dto

    def insert_department(self, department_dto):
        """
        Inserta un nuevo departamento usando un DepartmentDto.
        Args:
            department_dto (DepartmentDto): DTO con los datos del departamento.
        Returns:
            Department: Objeto Department insertado.
        """
        department = Department(
            department_id=department_dto.department_id or uuid.uuid4(),
            link=department_dto.link,
            address=department_dto.address,
            neighborhood=department_dto.neighborhood,
            photo_url=department_dto.photo_url,
            price=department_dto.price,
            price_currency=department_dto.price_currency,
            publication_date=department_dto.publication_date,
            title=department_dto.title,
            create_date=department_dto.create_date,
            department_code=department_dto.department_code
        )
        return self.repository.insert_department(department)

    def exists_department(self, **kwargs):
        """
        Verifica si existe un departamento según los campos clave.
        Args:
            kwargs: Campos clave para buscar el departamento.
        Returns:
            bool: True si existe, False si no.
        """
        return self.repository.exists_department(**kwargs)

    def get_nonexistent_department_codes(self, codes: list[str]) -> list[str]:
        """
        Dada una lista de department_code, retorna solo los que NO existen en la base de datos.
        Args:
            codes (list[str]): Lista de códigos a verificar.
        Returns:
            list[str]: Códigos que no existen en la base de datos.
        """
        return self.repository.get_nonexistent_department_codes(codes)

    def create_department(self, department_data):
        return self.repository.get_all(department_data)

    def update_department(self, department_id, department_data):
        return self.repository.get_all(department_id, department_data)

    def delete_department(self, department_id):
        return self.repository.get_all(department_id)