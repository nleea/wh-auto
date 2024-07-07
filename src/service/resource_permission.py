import http
from models import GenericResponseModel, ResourcePermissionInsertModel
from data_adapter import ResourcePermission
from sqlalchemy.exc import DatabaseError, NoResultFound


class ResourcePermissionService:
    MSG_CREATED_SUCCESS = "Created successfully"
    MSG_SUSPENDED = "Suspended successfully"
    MSG_OK = "Ok"

    ERROR_INVALID_CREDENTIALS = "Invalid credentials"
    ERROR_NOT_FOUND = "Not found"

    ERROR_SERVICE = "There was a erorr"

    @classmethod
    def create_resource_permission(
        cls, resource_permission: ResourcePermissionInsertModel
    ) -> GenericResponseModel:

        try:
            resource_permission_to_create = resource_permission.create_db_entity()
            resource_permission_data = ResourcePermission.create_resource_permission(
                resource_permission_to_create
            )

            return GenericResponseModel(
                status_code=http.HTTPStatus.CREATED,
                message=cls.MSG_CREATED_SUCCESS,
                data=resource_permission_data.build_response_model(),
            )
        except (DatabaseError, NoResultFound) as e:
            return GenericResponseModel(
                status_code=http.HTTPStatus.BAD_REQUEST,
                message=cls.ERROR_SERVICE,
                error=str(e),
                data=None,
            )

    @classmethod
    def list_permission_by_resource(cls, resource: int):
        try:
            permission_by_resource = ResourcePermission.list_permission_by_resource(
                resource
            )
            return GenericResponseModel(
                status_code=http.HTTPStatus.OK,
                message=cls.MSG_OK,
                data=permission_by_resource,
            )
        except Exception as e:
            return GenericResponseModel(
                status_code=http.HTTPStatus.BAD_REQUEST,
                message=cls.ERROR_SERVICE,
                error=str(e),
                data=None,
            )
