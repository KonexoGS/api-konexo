from app.core.session import Database
from app.models.user_model import *
from app.models.developers_model import *
from app.enums import UserType, Roles, DeveloperLevel
from app.service.user_service import UserService
from fastapi import HTTPException

class DeveloperService(UserService):
    def __init__(self):
        super().__init__()
        self.main_collection_name = "developers"
        self.project_collection_name = "projects"
        self.main_collection = super().get_collection_data(self.main_collection_name)
        self.project_collection = super().get_collection_data(self.project_collection_name)

    def insert_developer(self, user_response: DeveloperResponseModel):
        new_user = UserModel(
            full_name=user_response.full_name,
            username=user_response.username,
            email=user_response.email,
            password=user_response.password,
            user_type=UserType.DEVELOPER.value,
            social_medias=user_response.social_medias
        )
        new_user_id = super().insert_user(new_user)
        if not new_user_id:
            raise HTTPException(status_code=404, detail="Não foi possível adicionar o usuário")
        
        new_user.user_id = str(new_user_id)

        new_dev = DevelopersModel(
            stacks=user_response.stacks,
            speciality=user_response.speciality,
            user_id=new_user_id
        )

        new_dev_dict = new_dev.model_dump()
        new_dev_dict.pop('dev_id')
        new_dev_id = super().insert(self.main_collection_name, new_dev_dict)
        new_dev.dev_id = str(new_dev_id)

        return new_dev



        
