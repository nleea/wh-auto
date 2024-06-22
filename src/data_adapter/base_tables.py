from sqlalchemy import Column, String
from data_adapter.db import DBBase, DBBaseModel
from models.base_model import GenderModel, RolModel
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship

class Gender(DBBase, DBBaseModel):
    __tablename__ = "genders"

    name_gender = Column(String(100), nullable=False)

    def __to_model(self) -> GenderModel:
        """converts db orm object to pydantic model"""
        return GenderModel.model_validate(self)

    @classmethod
    def create_gender(cls, gender) -> GenderModel:
        from controller.context_manager import get_db_session

        db: Session = get_db_session()
        db.add(gender)
        db.flush()
        return gender.__to_model()

    @classmethod
    def get_by_id(cls, id) -> GenderModel:
        gender = super().get_by_id(id)
        return gender.__to_model() if gender else None


class Rol(DBBase, DBBaseModel):
    __tablename__ = "rol"

    name_rol = Column(String(100), nullable=False)

    def __to_model(self) -> RolModel:
        """converts db orm object to pydantic model"""
        return RolModel.model_validate(self)

    @classmethod
    def create_rol(cls, rol) -> RolModel:
        from controller.context_manager import get_db_session

        db: Session = get_db_session()
        db.add(rol)
        db.flush()
        return rol.__to_model()

    @classmethod
    def get_by_id(cls, id) -> RolModel:
        rol = super().get_by_id(id)
        return rol.__to_model() if rol else None
