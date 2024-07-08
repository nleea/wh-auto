import http
from models import GenericResponseModel, RolPermissionInsertModel
from data_adapter import RolPermission
from sqlalchemy.exc import DatabaseError, NoResultFound


class RolPermissionService:
    MSG_CREATED_SUCCESS = "Created successfully"
    MSG_SUSPENDED = "Suspended successfully"
    MSG_OK = "Ok"

    ERROR_INVALID_CREDENTIALS = "Invalid credentials"
    ERROR_NOT_FOUND = "Not found"

    ERROR_SERVICE = "There was a erorr"

    @classmethod
    def create_rol_permission(
        cls, rol_permission: RolPermissionInsertModel
    ) -> GenericResponseModel:

        try:
            print(rol_permission)
            rol_permission_to_create = rol_permission.create_db_entity()
            print(rol_permission_to_create)
            rol_permission_data = RolPermission.create_rol_permission(rol_permission_to_create)

            print(rol_permission_data)

            return GenericResponseModel(
                status_code=http.HTTPStatus.CREATED,
                message=cls.MSG_CREATED_SUCCESS,
                data=rol_permission_data.build_response_model(),
            )
        except (DatabaseError, NoResultFound) as e:
            return GenericResponseModel(
                status_code=http.HTTPStatus.BAD_REQUEST,
                message=cls.ERROR_SERVICE,
                error=str(e),
                data=None,
            )


    @classmethod
    def list_permission_by_rol(cls, rol: int):
        try:
            permission_by_rol = RolPermission.list_permission_by_rol(rol)
            return GenericResponseModel(
                status_code=http.HTTPStatus.OK,
                message=cls.MSG_OK,
                data=permission_by_rol,
            )
        except Exception as e:
            return GenericResponseModel(
                status_code=http.HTTPStatus.BAD_REQUEST,
                message=cls.ERROR_SERVICE,
                error=str(e),
                data=None,
            )
