from pydantic import BaseModel
from models.base import DBBaseModel
from typing import Optional


class PermissionsModelResponse(BaseModel):
    """Response Permission Model"""

    id: Optional[int]
    name: str

    class Config:
        from_attributes = True


class PermissionsInsertModel(BaseModel):
    """Permission insert model"""

    name: str

    def create_db_entity(self):
        from data_adapter import Permission

        dict_to_build_db_entity = self.model_dump()
        return Permission(**dict_to_build_db_entity)


class PermissionModel(DBBaseModel):
    """Permission Model"""

    name: str

    class Config:
        from_attributes = True

    def build_response_model(self) -> PermissionsModelResponse:
        return PermissionsModelResponse.model_validate(self.model_dump())
