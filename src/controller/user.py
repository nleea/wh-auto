import http

from fastapi import APIRouter, Depends, Request

from controller.context_manager import build_request_context
from models.base import GenericResponseModel
from models.user import UserInsertModel
from service.user_service import UserService
from utils.helpers import Check
from config.limiter import limiter

user_router = APIRouter(prefix="/v1/user", tags=["user"])
RESOURCE = "user"


@user_router.post(
    "/register",
    status_code=http.HTTPStatus.CREATED,
    response_model=GenericResponseModel,
    dependencies=[Depends(build_request_context), Depends(Check(RESOURCE, True))],
)
@limiter.limit("5/minute")
async def register_user(request: Request, user: UserInsertModel):
    response: GenericResponseModel = UserService.create_user(user=user)
    return response


@user_router.get(
    "/list",
    status_code=http.HTTPStatus.OK,
    response_model=GenericResponseModel,
    dependencies=[Depends(build_request_context), Depends(Check(RESOURCE, True))],
)
@limiter.limit("5/minute")
async def user_list(request: Request):
    response: GenericResponseModel = UserService.list_user()
    return response
