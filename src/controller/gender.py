import http

from fastapi import APIRouter, Depends, Request

from controller.context_manager import build_request_context
from models.base import GenericResponseModel
from models.base_model import GenderInsertModel
from service.gender_service import GenderService
from utils.helpers import Check
from config.limiter import limiter

gender_router = APIRouter(prefix="/v1/gender", tags=["gender"])
RESOURCE = "gender"


@gender_router.post(
    "/create",
    status_code=http.HTTPStatus.CREATED,
    response_model=GenericResponseModel,
    dependencies=[Depends(build_request_context), Depends(Check(RESOURCE, True))],
)
@limiter.limit("5/minutes")
async def create_gender(request: Request, gender: GenderInsertModel):
    response: GenericResponseModel = GenderService.create_gender(gender=gender)
    return response


@gender_router.get(
    "/list",
    status_code=http.HTTPStatus.OK,
    response_model=GenericResponseModel,
    dependencies=[Depends(build_request_context), Depends(Check(RESOURCE))],
)
@limiter.limit("5/minutes")
async def list_gender(request: Request):
    response: GenericResponseModel = GenderService.list_gender()
    return response
