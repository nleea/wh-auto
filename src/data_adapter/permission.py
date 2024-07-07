from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from data_adapter.db import DBBase, DBBaseModel
from models import (
    PermissionModel,
    RolPermissionModel,
    ResourcePermissionModel,
    PermissionsModelResponse,
    ResourceResponse
)
from data_adapter.base_tables import Rol
from data_adapter.resources import Resources
from sqlalchemy.orm import joinedload


class Permission(DBBase, DBBaseModel):

    __tablename__ = "permissions"

    name = Column(String(255), nullable=True)
    rol_permissions = relationship("RolPermission", back_populates="permission")

    def __to_model(self) -> PermissionModel:
        """converts db orm object to pydantic model"""
        return PermissionModel.model_validate(self)

    @classmethod
    def create_permission(cls, permissions) -> PermissionModel:
        from controller import get_db_session

        db = get_db_session()
        db.add(permissions)
        db.flush()

        return permissions.__to_model()

    @classmethod
    def list_permission(cls) -> list[PermissionModel]:
        from controller import get_db_session

        db = get_db_session()
        permissions = db.query(cls).all()
        return [x.__to_model() for x in permissions]


class RolPermission(DBBase, DBBaseModel):

    __tablename__ = "rol_permissions"

    permission_id = Column(Integer, ForeignKey("permissions.id"))
    permission = relationship("Permission", back_populates="rol_permissions")

    rol_id = Column(Integer, ForeignKey("rol.id"))
    rol = relationship("Rol", back_populates="rol_permissions")

    def __to_model(self) -> RolPermissionModel:
        """converts db orm object to pydantic model"""
        return RolPermissionModel.model_validate(self)

    @classmethod
    def create_rol_permission(cls, permissions) -> RolPermissionModel:
        from controller import get_db_session

        db = get_db_session()
        db.add(permissions)
        db.flush()

        return permissions.__to_model()

    @classmethod
    def list_rol_permission(cls) -> list[RolPermissionModel]:
        from controller import get_db_session

        db = get_db_session()
        permissions = db.query(cls).all()
        return [x.__to_model() for x in permissions]

    @classmethod
    def list_permission_by_rol(cls, rol: int):
        from controller import get_db_session

        db = get_db_session()

        permission_by_rol = (
            db.query(Rol)
            .options(
                joinedload(Rol.rol_permissions).joinedload(RolPermission.permission)
            )
            .filter(Rol.id == rol)
            .one_or_none()
        )

        if permission_by_rol is None:
            return []

        permission = [
            rol_permission.permission
            for rol_permission in permission_by_rol.rol_permissions
        ]

        return [PermissionsModelResponse.model_validate(x) for x in permission]


class ResourcePermission(DBBase, DBBaseModel):

    __tablename__ = "resource_permissions"

    permission_id = Column(Integer, ForeignKey("permissions.id"))
    permission = relationship("Permission")

    resource_id = Column(Integer, ForeignKey("resources.id"))
    resource = relationship("Resources")

    def __to_model(self) -> ResourcePermissionModel:
        """converts db orm object to pydantic model"""
        return ResourcePermissionModel.model_validate(self)

    @classmethod
    def create_resource_permission(cls, permissions) -> ResourcePermissionModel:
        from controller import get_db_session

        db = get_db_session()
        db.add(permissions)
        db.flush()

        return permissions.__to_model()

    @classmethod
    def list_resource_permission(cls) -> list[ResourcePermissionModel]:
        from controller import get_db_session

        db = get_db_session()
        permissions = db.query(cls).all()
        return [x.__to_model() for x in permissions]

    @classmethod
    def list_permission_by_resource(cls, resource: int):
        from controller import get_db_session

        db = get_db_session()

        permission_by_resource = (
            db.query(Rol)
            .options(
                joinedload(Resources.permission_resources).joinedload(ResourcePermission.resource)
            )
            .filter(Resources.id == resource)
            .one_or_none()
        )

        if permission_by_resource is None:
            return []

        resources = [
            resource_permission.resource
            for resource_permission in permission_by_resource.permission_resources
        ]

        return [ResourceResponse.model_validate(x) for x in resources]
