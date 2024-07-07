import http
from models import GenericResponseModel, PermissionsInsertModel
from data_adapter import Permission
from sqlalchemy.exc import DatabaseError, NoResultFound


class PermissionService:
    MSG_CREATED_SUCCESS = "Created successfully"
    MSG_SUSPENDED = "Suspended successfully"
    MSG_OK = "Ok"

    ERROR_INVALID_CREDENTIALS = "Invalid credentials"
    ERROR_NOT_FOUND = "Not found"

    ERROR_SERVICE = "There was a erorr"

    @classmethod
    def create_permission(
        cls, permission: PermissionsInsertModel
    ) -> GenericResponseModel:

        try:
            permission_to_create = permission.create_db_entity()
            
            resource_data = Permission.create_permission(permission_to_create)

            return GenericResponseModel(
                status_code=http.HTTPStatus.CREATED,
                message=cls.MSG_CREATED_SUCCESS,
                data=resource_data.build_response_model(),
            )
        except (DatabaseError, NoResultFound) as e:
            return GenericResponseModel(
                status_code=http.HTTPStatus.BAD_REQUEST,
                message=cls.ERROR_SERVICE,
                error=str(e),
                data=None,
            )

    @classmethod
    def list_permissions(cls) -> GenericResponseModel:
        try:
            rol_list = Permission.list_permission()

            return GenericResponseModel(
                status_code=http.HTTPStatus.OK,
                message=cls.MSG_OK,
                data=[x.build_response_model() for x in rol_list],
            )
        except Exception as e:
            return GenericResponseModel(
                status_code=http.HTTPStatus.BAD_REQUEST,
                message=cls.ERROR_SERVICE,
                error=str(e),
                data=None,
            )
