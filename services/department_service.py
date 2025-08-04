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

    def create_department(self, department_data):
        return self.repository.get_all(department_data)

    def update_department(self, department_id, department_data):
        return self.repository.get_all(department_id, department_data)

    def delete_department(self, department_id):
        return self.repository.get_all(department_id)