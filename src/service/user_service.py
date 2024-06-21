import http
from models.base import GenericResponseModel
from models.user import UserInsertModel
from utils.password_hasher import PasswordHasher
from data_adapter.user import User
from logger import logger

class UserService:
    MSG_USER_CREATED_SUCCESS = "User created successfully"
    MSG_USER_LOGIN_SUCCESS = "Login successful"
    MSG_USER_SUSPENDED = "User is suspended successfully"

    ERROR_INVALID_CREDENTIALS = "Invalid credentials"
    ERROR_USER_NOT_FOUND = "User not found"

    @classmethod
    def create_user(cls, user: UserInsertModel) -> GenericResponseModel:
        hasher = PasswordHasher()

        hashed_password = hasher.hash_password(user.password)
        user_to_create = user.create_db_entity(password_hash=hashed_password)
        user_data = User.create_user(user_to_create)

        return GenericResponseModel(
            status_code=http.HTTPStatus.CREATED,
            message=cls.MSG_USER_CREATED_SUCCESS,
            data=user_data.build_response_model(),
        )
