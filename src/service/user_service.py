import http
from models import GenericResponseModel, UserInsertModel, PersonInsertModel
from utils import PasswordHasher
from data_adapter import User, Person


class UserService:
    MSG_USER_CREATED_SUCCESS = "User created successfully"
    MSG_USER_LOGIN_SUCCESS = "Login successful"
    MSG_USER_SUSPENDED = "User is suspended successfully"
    MSG_USER_OK = "Ok"

    ERROR_INVALID_CREDENTIALS = "Invalid credentials"
    ERROR_USER_NOT_FOUND = "User not found"

    ERROR_SERVICE = "There was a erorr"

    @classmethod
    def create_user(cls, user: UserInsertModel) -> GenericResponseModel:
        try:
            hasher = PasswordHasher()

            person_to_insert = PersonInsertModel(
                age=user.age,
                name=user.name,
                last_name=user.last_name,
                phone_number=user.phone_number,
                gender=user.gender,
            )

            person_create = Person.create_person(person_to_insert)

            hashed_password = hasher.hash_password(user.password)
            user.person = person_create.id
            user_to_create = user.create_db_entity(password_hash=hashed_password)

            user_data = User.create_user(user_to_create)

            return GenericResponseModel(
                status_code=http.HTTPStatus.CREATED,
                message=cls.MSG_USER_CREATED_SUCCESS,
                data=user_data.build_response_model(),
            )
        except Exception as e:
            return GenericResponseModel(
                status_code=http.HTTPStatus.BAD_REQUEST,
                message=cls.ERROR_SERVICE,
                error=str(e),
                data=None,
            )

    @classmethod
    def list_user(cls) -> GenericResponseModel:
        try:
            users = User.list_user()

            return GenericResponseModel(
                status_code=http.HTTPStatus.OK,
                message=cls.MSG_USER_OK,
                data=[x.build_response_model() for x in users],
            )
        except Exception as e:
            return GenericResponseModel(
                status_code=http.HTTPStatus.BAD_REQUEST,
                message=cls.ERROR_SERVICE,
                error=str(e),
                data=None,
            )
