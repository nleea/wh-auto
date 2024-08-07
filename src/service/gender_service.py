import http
from models import GenericResponseModel, GenderInsertModel
from data_adapter import Gender


class GenderService:
    MSG_CREATED_SUCCESS = "Created successfully"
    MSG_SUSPENDED = "Suspended successfully"
    MSG_OK = "Ok"

    ERROR_INVALID_CREDENTIALS = "Invalid credentials"
    ERROR_NOT_FOUND = "Not found"
    ERROR_SERVICE = "There was a erorr"
    

    @classmethod
    def create_gender(cls, gender: GenderInsertModel) -> GenericResponseModel:

        try:
            gender_to_create = gender.create_db_entity()
            gender_data = Gender.create_gender(gender_to_create)

            return GenericResponseModel(
                status_code=http.HTTPStatus.CREATED,
                message=cls.MSG_CREATED_SUCCESS,
                data=gender_data.build_response_model(),
            )
        except Exception as e:
            return GenericResponseModel(
                status_code=http.HTTPStatus.BAD_REQUEST,
                message=cls.ERROR_SERVICE,
                error=str(e),
                data=None,
            )

    @classmethod
    def list_gender(cls) -> GenericResponseModel:

        try:
            list_gender = Gender.list_genders()

            return GenericResponseModel(
                status_code=http.HTTPStatus.OK,
                message=cls.MSG_OK,
                data=[x.build_response_model() for x in list_gender],
            )
        except Exception as e:
            return GenericResponseModel(
                status_code=http.HTTPStatus.BAD_REQUEST,
                message=cls.ERROR_SERVICE,
                error=str(e),
                data=None,
            )
