from pydantic import BaseModel
from models.base import DBBaseModel
from typing import Optional

class ResourceResponse(BaseModel):
    """Response Resource Model"""
    id: Optional[int]
    path: str
    name: str
    parent_id: int | None = None
    
    class Config:
        from_attributes = True


class ResourceInsertModel(BaseModel):
    """Resource insert model"""

    path: str
    name: str
    parent_id: int | None = None

    def create_db_entity(self):
        from data_adapter import Resources

        dict_to_build_db_entity = self.model_dump()
        return Resources(**dict_to_build_db_entity)


class ResourceModel(DBBaseModel):
    """Resource Model"""

    path: str
    name: str
    parent_id: int | None = None

    class Config:
        from_attributes = True
    
    
    def build_response_model(self) -> ResourceResponse:
        return ResourceResponse.model_validate(self.model_dump())
