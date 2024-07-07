from pydantic import BaseModel
from models.base import DBBaseModel
from models import ResourceResponse, PermissionsModelResponse


class ResourcePermissionResponse(BaseModel):
    """Response Resource-Permission Model"""

    permission: PermissionsModelResponse
    resource: ResourceResponse

    class Config:
        from_attributes = True


class ResourcePermissionInsertModel(BaseModel):
    """Insert Resource-Permission Model"""

    permission: int
    resource: int

    def create_db_entity(self):
        from data_adapter import ResourcePermission

        dict_to_build_db_entity = self.model_dump()
        dict_to_build_db_entity["permission_id"] = self.permission
        dict_to_build_db_entity["resource_id"] = self.resource

        del dict_to_build_db_entity["permission"]
        del dict_to_build_db_entity["resource"]

        return ResourcePermission(**dict_to_build_db_entity)


class ResourcePermissionModel(DBBaseModel):
    """Resource-Permission Model"""

    permission: PermissionsModelResponse
    resource: ResourceResponse

    class Config:
        from_attributes = True

    def build_response_model(self) -> ResourcePermissionResponse:
        return ResourcePermissionResponse.model_validate(self.model_dump())
