from app.core.session import Database
from bson import ObjectId


class ProjectService(Database):
    def __init__(self):
        super().__init__()
        self.main_collection_name = "projects"
        self.dev_collection_name = "developers"
        self.main_collection = super().get_collection_data(self.main_collection_name)
        self.dev_collection = super().get_collection_data(self.dev_collection_name)

    
    def find_by_project_name(self, project_name: str):
        if not isinstance(project_name, str):
            raise ValueError("O nome do projeto deve ser string")
        project = self.main_collection.find({"name": project_name, "is_deleted": False})
        
        return project
    
    def find_by_friendly_code(self, friendly_code: str):
        if not isinstance(friendly_code, str):
            raise ValueError("O código do projeto deve ser uma string")
        project = self.main_collection.find_one({
            "friendly_code": friendly_code, 
            "is_deleted": False})

        return project
    

    def find_projects_by_developer_id(self, dev_id: str | ObjectId):
        if not isinstance(dev_id, str):
            raise ValueError("O ID do desenvolvedor deve ser string")
        dev_id = super().validate_object_id(dev_id)

        developer = super().find_by_id(
            collection_name="developers", 
            data_id=str(dev_id))
        
        if not developer:
            raise ValueError(f"Desenvolvedor com id '{dev_id}' não existe no sistema.")
        projects_from_dev = [
            self.main_collection.find(
                {"developers_id": developer['_id'], 
                "is_deleted": False})
            ]

        return projects_from_dev

        
    def find_projects_by_owner(self, owner_id: str | ObjectId):
        if not isinstance(owner_id, str):
            raise ValueError("O ID do proprietário deve ser uma string")
        owner_id = super().validate_object_id(owner_id)

        owner = self.user_collection.find_one({   
                "_id": owner_id, 
                "is_deleted": False
            })
        if not owner:
            raise ValueError(f"Usuário com ID '{owner_id}' não existe no sistema.")
        
        
        return self.main_collection.find({
                "_id": owner['_id'],
                "is_deleted": False
            })

    def find_projects_by_category(self, category: str):
        if not isinstance(category, str):
            raise ValueError("A categoria deve ser uma string")
        project = self.main_collection.find({
            "category": category,
            "is_deleted": False
        })

        return project