import http
from models.base import GenericResponseModel
from models.base_model import RolInsertModel
from data_adapter.base_tables import Rol


class RolService:
    MSG_CREATED_SUCCESS = "Created successfully"
    MSG_SUSPENDED = "Suspended successfully"

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