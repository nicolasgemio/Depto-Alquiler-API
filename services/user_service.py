from repositories.user_repository import UserRepository
from dtos.user_dto import UserDto
from models.user import User
from uuid import UUID
import uuid

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user(self, google_id: str) -> UserDto | None:
        if google_id is None or google_id == "":
            return []
        
        user = self.repository.get_by_google_id(google_id)

        return user

    def create_user(self, user_info_dic):
        new_user = User(
            user_id = uuid.uuid4(),
            google_id = user_info_dic.get('sub'),
            given_name = user_info_dic.get('given_name'),
            family_name = user_info_dic.get('family_name'),
            email = user_info_dic.get('email')
        )
        self.repository.create_user(new_user)