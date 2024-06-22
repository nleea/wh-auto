import http

from fastapi import APIRouter, Depends

from controller.context_manager import build_request_context
from models.base import GenericResponseModel
from models.base_model import RolInsertModel
from service.rol_service import RolService
from utils.helpers import build_api_response

rol_router = APIRouter(prefix="/v1/rol", tags=["rol"])


@rol_router.post(
    "/create",
    status_code=http.HTTPStatus.CREATED,
    response_model=GenericResponseModel,
)
async def create_rol(rol: RolInsertModel, _=Depends(build_request_context)):
    response: GenericResponseModel = RolService.create_rol(rol=rol)
    return build_api_response(response)
