from models.base import DBBaseModel
from pydantic import BaseModel
from models import GenderModel, GenderResponseModel


class PersonResponseModel(BaseModel):
    """Response Person Model"""

    name: str
    last_name: str
    age: int
    phone_number: str
    gender: GenderResponseModel


class PersonInsertModel(BaseModel):
    """Insert Person Model"""

    name: str
    last_name: str
    age: int
    phone_number: str
    gender: str | int

    def create_db_entity(self):
        from data_adapter import Person

        dict_to_build_db_entity = self.model_dump()
        dict_to_build_db_entity["gender_id"] = self.gender
        del dict_to_build_db_entity["gender"]
        return Person(**dict_to_build_db_entity)


class PersonModel(DBBaseModel):
    """Person Model"""

    name: str
    last_name: str
    age: int
    phone_number: str
    gender: GenderModel

    class Config:
        from_attributes = True
        
    def model_dump(self, **kwargs):
        kwargs.setdefault("updated_at", True)
        return super().model_dump(**kwargs)
