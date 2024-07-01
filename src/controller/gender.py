import http

from fastapi import APIRouter, Depends

from controller.context_manager import build_request_context
from models.base import GenericResponseModel
from models.base_model import GenderInsertModel
from service.gender_service import GenderService

gender_router = APIRouter(prefix="/v1/gender", tags=["gender"])


@gender_router.post(
    "/create",
    status_code=http.HTTPStatus.CREATED,
    response_model=GenericResponseModel,
)
async def create_gender(gender: GenderInsertModel, _=Depends(build_request_context)):
    response: GenericResponseModel = GenderService.create_gender(gender=gender)
    return response


@gender_router.get(
    "/list", status_code=http.HTTPStatus.OK, response_model=GenericResponseModel
)
async def list_gender(_=Depends(build_request_context)):
    response: GenericResponseModel = GenderService.list_gender()
    return response
