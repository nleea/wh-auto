import http

from fastapi import APIRouter, Depends

from controller.context_manager import build_request_context
from models.base import GenericResponseModel
from models.user import UserInsertModel
from service.user_service import UserService

user_router = APIRouter(prefix="/v1/user", tags=["user"])


@user_router.post(
    "/register",
    status_code=http.HTTPStatus.CREATED,
    response_model=GenericResponseModel,
)
async def register_user(user: UserInsertModel, _=Depends(build_request_context)):
    response: GenericResponseModel = UserService.create_user(user=user)
    return response


@user_router.get(
    "/list",
    status_code=http.HTTPStatus.OK,
    response_model=GenericResponseModel,
)
async def user_list(_=Depends(build_request_context)):
    response: GenericResponseModel = UserService.list_user()
    return response
