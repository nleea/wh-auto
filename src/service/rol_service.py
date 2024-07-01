import http
from models import GenericResponseModel, RolInsertModel
from data_adapter import Rol


class RolService:
    MSG_CREATED_SUCCESS = "Created successfully"
    MSG_SUSPENDED = "Suspended successfully"
    MSG_OK = "Ok"

    ERROR_INVALID_CREDENTIALS = "Invalid credentials"
    ERROR_NOT_FOUND = "Not found"

    @classmethod
    def create_rol(cls, rol: RolInsertModel) -> GenericResponseModel:

        rol_to_create = rol.create_db_entity()
        rol_data = Rol.create_rol(rol_to_create)

        return GenericResponseModel(
            status_code=http.HTTPStatus.CREATED,
            message=cls.MSG_CREATED_SUCCESS,
            data=rol_data.build_response_model(),
        )

    @classmethod
    def list_rol(cls) -> GenericResponseModel:
        rol_list = Rol.list_roles()

        return GenericResponseModel(
            status_code=http.HTTPStatus.OK,
            message=cls.MSG_OK,
            data=[x.build_response_model() for x in rol_list],
        )
