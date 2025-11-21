from app.core.session import Database
from app.models.user_model import *
from app.models.developers_model import *
from app.enums import UserType, Roles, DeveloperLevel
from app.service.user_service import UserService
from app.service.auth_service import AuthService
from fastapi import HTTPException, UploadFile, File

class DeveloperService(UserService):
    def __init__(self):
        super().__init__()
        self.main_collection_name = "developers"
        self.project_collection_name = "projects"
        self.main_collection = super().get_collection_data(self.main_collection_name)
        self.project_collection = super().get_collection_data(self.project_collection_name)
        self._auth_service = AuthService()

    def insert_developer(self, user_response: DeveloperResponseModel, profile_photo: UploadFile = File(None)):
        new_user = UserModel(
            full_name=user_response.full_name,
            username=user_response.username,
            email=user_response.email,
            password=self._auth_service.hash_password(user_response.password),
            headline=user_response.headline,
            address=user_response.address,
            user_type=UserType.DEVELOPER.value,
            social_medias=user_response.social_medias
        )
        new_user_id = super().insert_user(new_user)
        if not new_user_id:
            raise HTTPException(status_code=404, detail="Não foi possível adicionar o usuário")
        
        new_user.user_id = str(new_user_id)

        new_dev = DevelopersModel(
            tech_skills=user_response.tech_skills,
            soft_skills=user_response.soft_skills,
            experience=user_response.experience,
            dev_level=user_response.dev_level,
            languages=user_response.languages,
            user_id=new_user_id
        )

        new_dev_dict = new_dev.model_dump()
        new_dev_dict.pop('dev_id')
        new_dev_id = super().insert(self.main_collection_name, new_dev_dict)
        new_dev.dev_id = str(new_dev_id)

        return new_dev



        
