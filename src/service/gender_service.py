import http
from models import GenericResponseModel, GenderInsertModel
from data_adapter import Gender


class GenderService:
    MSG_CREATED_SUCCESS = "Created successfully"
    MSG_SUSPENDED = "Suspended successfully"

    ERROR_INVALID_CREDENTIALS = "Invalid credentials"
    ERROR_NOT_FOUND = "Not found"

    @classmethod
    def create_gender(cls, gender: GenderInsertModel) -> GenericResponseModel:

        gender_to_create = gender.create_db_entity()
        gender_data = Gender.create_gender(gender_to_create)

        return GenericResponseModel(
            status_code=http.HTTPStatus.CREATED,
            message=cls.MSG_CREATED_SUCCESS,
            data=gender_data.build_response_model(),
        )
