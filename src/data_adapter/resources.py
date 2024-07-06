from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from data_adapter.db import DBBase, DBBaseModel
from models import ResourceModel, RolResourceModel, ResourceResponse
from data_adapter.base_tables import Rol
from sqlalchemy.orm import joinedload


class Resources(DBBase, DBBaseModel):

    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    path = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=True)
    parent_id = Column(Integer, ForeignKey("resources.id"), nullable=True)
    children = relationship("Resources", backref="parent", remote_side=[id])
    rol_resources = relationship("RolResources", back_populates="resource")

    def __to_model(self) -> ResourceModel:
        """converts db orm object to pydantic model"""
        return ResourceModel.model_validate(self)

    @classmethod
    def create_resource(cls, resource) -> ResourceModel:
        from controller import get_db_session

        db = get_db_session()
        db.add(resource)
        db.flush()

        return resource.__to_model()

    @classmethod
    def list_resources(cls) -> list[ResourceModel]:
        from controller import get_db_session

        db = get_db_session()
        resources = db.query(cls).all()
        return [x.__to_model() for x in resources]


class RolResources(DBBase, DBBaseModel):

    __tablename__ = "rol_resource"

    resource_id = Column(Integer, ForeignKey("resources.id"))
    resource = relationship("Resources", back_populates="rol_resources")

    rol_id = Column(Integer, ForeignKey("rol.id"))
    rol = relationship("Rol", back_populates="rol_resources")

    def __to_model(self) -> ResourceModel:
        """converts db orm object to pydantic model"""
        return RolResourceModel.model_validate(self)

    @classmethod
    def create_rol_resource(cls, rol_resource) -> RolResourceModel:
        from controller import get_db_session

        db = get_db_session()
        db.add(rol_resource)
        db.flush()

        return rol_resource.__to_model()

    @classmethod
    def list_rol_resources(cls) -> list[RolResourceModel]:
        from controller import get_db_session

        db = get_db_session()
        resources = db.query(cls).all()
        return [x.__to_model() for x in resources]

    @classmethod
    def list_resouce_by_rol(cls, rol: int):
        from controller import get_db_session

        db = get_db_session()

        resouces_by_rol = (
            db.query(Rol)
            .options(joinedload(Rol.rol_resources).joinedload(RolResources.resource))
            .filter(Rol.id == rol)
            .one_or_none()
        )

        if resouces_by_rol is None:
            return []

        resources = [
            rol_resource.resource for rol_resource in resouces_by_rol.rol_resources
        ]

        return [ResourceResponse.model_validate(x) for x in resources]
