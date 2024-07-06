import http
from models import GenericResponseModel, RolResourceInsertModel
from data_adapter import RolResources
from sqlalchemy.exc import DatabaseError, NoResultFound


class RolResourceService:
    MSG_CREATED_SUCCESS = "Created successfully"
    MSG_SUSPENDED = "Suspended successfully"
    MSG_OK = "Ok"

    ERROR_INVALID_CREDENTIALS = "Invalid credentials"
    ERROR_NOT_FOUND = "Not found"

    ERROR_SERVICE = "There was a erorr"

    @classmethod
    def create_rol_resource(
        cls, resource: RolResourceInsertModel
    ) -> GenericResponseModel:

        try:
            resource_to_create = resource.create_db_entity()
            resource_data = RolResources.create_rol_resource(resource_to_create)

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
    def list_rol_resources(cls) -> GenericResponseModel:
        try:
            rol_list = RolResources.list_rol_resources()

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

    @classmethod
    def list_resources_by_rol(cls, rol: int):
        try:
            resource_by_rol = RolResources.list_resouce_by_rol(rol)
            return GenericResponseModel(
                status_code=http.HTTPStatus.OK,
                message=cls.MSG_OK,
                data=resource_by_rol,
            )
        except Exception as e:
            return GenericResponseModel(
                status_code=http.HTTPStatus.BAD_REQUEST,
                message=cls.ERROR_SERVICE,
                error=str(e),
                data=None,
            )
