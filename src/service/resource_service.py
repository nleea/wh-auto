import http
from models import GenericResponseModel, ResourceInsertModel
from data_adapter import Resources


class ResourceService:
    MSG_CREATED_SUCCESS = "Created successfully"
    MSG_SUSPENDED = "Suspended successfully"
    MSG_OK = "Ok"

    ERROR_INVALID_CREDENTIALS = "Invalid credentials"
    ERROR_NOT_FOUND = "Not found"

    ERROR_SERVICE = "There was a erorr"

    @classmethod
    def create_resource(cls, resource: ResourceInsertModel) -> GenericResponseModel:

        try:
            resource_to_create = resource.create_db_entity()
            resource_data = Resources.create_resource(resource_to_create)

            return GenericResponseModel(
                status_code=http.HTTPStatus.CREATED,
                message=cls.MSG_CREATED_SUCCESS,
                data=resource_data.build_response_model(),
            )
        except Exception as e:
            return GenericResponseModel(
                status_code=http.HTTPStatus.BAD_REQUEST,
                message=cls.ERROR_SERVICE,
                error=str(e),
                data=None,
            )

    @classmethod
    def list_resources(cls) -> GenericResponseModel:
        try:
            rol_list = Resources.list_resources()

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
