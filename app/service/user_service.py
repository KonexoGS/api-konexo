from app.core.session import Database
from app.models.user_model import UserModel
from fastapi import HTTPException

class UserService(Database):
    def __init__(self):
        super().__init__()
        self.user_collection_name = "users"
        self.user_collection = super().get_collection_data(self.user_collection_name)
    
    def insert_user(self, new_user: UserModel):
        if not isinstance(new_user, UserModel):
            raise ValueError("O novo usuário deve ser do modelo UserModel")

        new_user_dict = new_user.model_dump()
        new_user_dict.pop('user_id')
        new_user_id = super().insert(self.user_collection_name, new_user_dict)

        if not new_user_id:
            raise Exception(f"Não foi possível adicionar o usuário {new_user_dict['user_type']}")
        return new_user_id

    def find_user_by_login(self, user_email: str | None):
        if not isinstance(user_email, str):
            raise ValueError("O novo usuário deve ser do modelo UserModel")
        
        user = self.user_collection.find_one({"email": user_email})
        if not user:
            raise HTTPException(status_code=404, detail=f"Nenhum usuário com email {user_email} foi encontrado")
        return user
        