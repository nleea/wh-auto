import http

from fastapi import APIRouter, Depends

from controller.context_manager import build_request_context
from models.base import GenericResponseModel
from models.user import UserInsertModel
from service.user_service import UserService
from utils.helpers import Check

user_router = APIRouter(prefix="/v1/user", tags=["user"])
RESOURCE = "user"


@user_router.post(
    "/register",
    status_code=http.HTTPStatus.CREATED,
    response_model=GenericResponseModel,
    dependencies=[Depends(build_request_context), Depends(Check(RESOURCE, True))],
)
async def register_user(user: UserInsertModel):
    response: GenericResponseModel = UserService.create_user(user=user)
    return response


@user_router.get(
    "/list",
    status_code=http.HTTPStatus.OK,
    response_model=GenericResponseModel,
    dependencies=[Depends(build_request_context), Depends(Check(RESOURCE, True))],
)
async def user_list():
    response: GenericResponseModel = UserService.list_user()
    return response
