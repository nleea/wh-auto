import http

from fastapi import APIRouter, Depends, Request

from controller.context_manager import build_request_context
from models.base import GenericResponseModel
from models.user import UserLoginModel
from service.auth_service import AuthService
from config.limiter import limiter

auth_router = APIRouter(prefix="/v1/auth", tags=["auth"])


@auth_router.post(
    "/login",
    status_code=http.HTTPStatus.OK,
    response_model=GenericResponseModel,
)
@limiter.limit("5/minutes")
async def register_user(
    request: Request, user: UserLoginModel, _=Depends(build_request_context)
):
    response: GenericResponseModel = AuthService.login(user_login=user)
    return response
