import http

from fastapi import APIRouter, Depends

from controller.context_manager import build_request_context
from models.base import GenericResponseModel
from models.user import UserLoginModel
from service.auth_service import AuthService

auth_router = APIRouter(prefix="/v1/auth", tags=["auth"])


@auth_router.post(
    "/login",
    status_code=http.HTTPStatus.OK,
    response_model=GenericResponseModel,
)
async def register_user(user: UserLoginModel, _=Depends(build_request_context)):
    response: GenericResponseModel = AuthService.login(user_login=user)
    return response
