from dependency_injector import containers, providers
from repositories.department_repository import DepartmentRepository
from repositories.user_repository import UserRepository
from repositories.search_repository import SearchRepository
from services.department_service import DepartmentService
from services.user_service import UserService
from services.search_service import SearchService   

class Container(containers.DeclarativeContainer):
    user_repository = providers.Singleton(UserRepository)
    search_repository = providers.Singleton(SearchRepository)
    department_repository = providers.Singleton(DepartmentRepository)
    
    user_service = providers.Singleton(UserService, repository=user_repository)
    search_service = providers.Singleton(SearchService, repository=search_repository)
    department_service = providers.Singleton(DepartmentService, repository=department_repository, user_service=user_service, search_service=search_service)
