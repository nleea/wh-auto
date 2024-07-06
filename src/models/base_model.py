from models.base import DBBaseModel
from pydantic import BaseModel
from typing import Optional

class GenderResponseModel(BaseModel):
    id: Optional[int]
    name_gender: str
    
    class Config:
        from_attributes = True


class GenderInsertModel(BaseModel):
    """Insert Gender Model"""

    name_gender: str

    def create_db_entity(self):
        from data_adapter import Gender

        dict_to_build_db_entity = self.model_dump()
        return Gender(**dict_to_build_db_entity)


class GenderModel(DBBaseModel):
    """Gender Model"""

    name_gender: str

    class Config:
        from_attributes = True

    def build_response_model(self) -> GenderResponseModel:
        return GenderResponseModel.model_validate(self.model_dump())


class RolInsertModel(BaseModel):
    """Insert Gender Model"""

    name_rol: str

    def create_db_entity(self):
        from data_adapter import Rol

        dict_to_build_db_entity = self.model_dump()
        return Rol(**dict_to_build_db_entity)


class RolResponseModel(BaseModel):
    id: Optional[int]
    name_rol: str
    
    class Config:
        from_attributes = True


class RolModel(DBBaseModel):
    """Rol Model"""

    name_rol: str

    class Config:
        from_attributes = True

    def build_response_model(self) -> RolResponseModel:
        return RolResponseModel.model_validate(self.model_dump())
