from pydantic import BaseModel
from models.base import DBBaseModel
from models import PermissionsModelResponse, RolResponseModel


class RolPermissionResponse(BaseModel):
    """Response Rol-Permission Model"""

    rol: RolResponseModel
    permission: PermissionsModelResponse

    class Config:
        from_attributes = True


class RolPermissionInsertModel(BaseModel):
    """Insert Rol-Permission Model"""

    rol: int
    permission: int

    def create_db_entity(self):
        from data_adapter import RolPermission

        dict_to_build_db_entity = self.model_dump()
        dict_to_build_db_entity["rol_id"] = self.rol
        dict_to_build_db_entity["permission_id"] = self.permission

        del dict_to_build_db_entity["rol"]
        del dict_to_build_db_entity["permission"]

        return RolPermission(**dict_to_build_db_entity)


class RolPermissionModel(DBBaseModel):
    """Rol-Permission Model"""

    rol: RolResponseModel
    permission: PermissionsModelResponse

    class Config:
        from_attributes = True

    def build_response_model(self) -> RolPermissionResponse:
        return RolPermissionResponse.model_validate(self.model_dump())
