from pydantic import BaseModel
from models.base import DBBaseModel
from models import ResourceResponse, RolResponseModel


class RolResourceResponse(BaseModel):
    """Response Rol-Resource Model"""

    rol: RolResponseModel
    resource: ResourceResponse


class RolResourceInsertModel(BaseModel):
    """Insert Rol-Resource Model"""

    rol: int
    resource: int

    def create_db_entity(self):
        from data_adapter import RolResources

        dict_to_build_db_entity = self.model_dump()
        dict_to_build_db_entity["rol_id"] = self.rol
        dict_to_build_db_entity["resource_id"] = self.resource

        del dict_to_build_db_entity["rol"]
        del dict_to_build_db_entity["resource"]

        return RolResources(**dict_to_build_db_entity)

class RolResourceModel(DBBaseModel):
    """Rol-Resource Model"""

    rol: RolResponseModel
    resource: ResourceResponse

    class Config:
        from_attributes = True
    
    
    def build_response_model(self) -> RolResourceResponse:
        return RolResourceResponse.model_validate(self.model_dump())