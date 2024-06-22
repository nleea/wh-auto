import http

from fastapi import APIRouter, Depends

from controller.context_manager import build_request_context
from models.base import GenericResponseModel
from models.base_model import GenderInsertModel
from service.gender_service import GenderService
from utils.helpers import build_api_response

gender_router = APIRouter(prefix="/v1/gender", tags=["gender"])


@gender_router.post(
    "/create",
    status_code=http.HTTPStatus.CREATED,
    response_model=GenericResponseModel,
)
async def create_gender(gender: GenderInsertModel, _=Depends(build_request_context)):
    response: GenericResponseModel = GenderService.create_gender(gender=gender)
    return build_api_response(response)
