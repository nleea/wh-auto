import http

from models import UserLoginModel, GenericResponseModel, UserTokenResponseModel
from data_adapter import User
from utils.password_hasher import PasswordHasher
from data_adapter.resources import RolResources


class AuthService:
    MSG_OK = "Login successful"
    MSG_FAILED = "User Not Found"
    MSG_PASSWORD_FAILD = "Password don't match"
    ERROR_SERVICE = "There was a erorr"

    @classmethod
    def login(cls, user_login: UserLoginModel) -> GenericResponseModel:
        try:
            from utils.jwt_handler import JWTHandler

            hasher = PasswordHasher()

            user = User.get_active_user_by_email(user_login.email)

            if not user:
                return GenericResponseModel(
                    message=cls.MSG_FAILED,
                    status_code=http.HTTPStatus.UNAUTHORIZED,
                )

            if not hasher.compare_password(
                encrypted_password=user.password_hash,
                plain_password=user_login.password,
            ):
                return GenericResponseModel(
                    message=cls.MSG_PASSWORD_FAILD,
                    status_code=http.HTTPStatus.UNAUTHORIZED,
                    data={},
                )

            token = JWTHandler.create_access_token({"uuid": str(user.uuid)})

            return GenericResponseModel(
                message=cls.MSG_OK,
                status_code=http.HTTPStatus.OK,
                data=UserTokenResponseModel(
                    user_uuid=user.uuid,
                    access_token=token,
                    user_role=str(user.rol.name_rol),
                    user_status=user.status,
                    resources=RolResources.list_resouce_by_rol(user.rol.id),
                ),
            )
        except Exception as e:
            return GenericResponseModel(
                status_code=http.HTTPStatus.BAD_REQUEST,
                message=cls.ERROR_SERVICE,
                error=str(e),
                data=None,
            )
