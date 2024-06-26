import http

from fastapi import APIRouter, Depends

from controller.context_manager import build_request_context
from models.base import GenericResponseModel
from models.base_model import RolInsertModel
from service.rol_service import RolService

rol_router = APIRouter(prefix="/v1/rol", tags=["rol"])


@rol_router.post(
    "/create",
    status_code=http.HTTPStatus.CREATED,
    response_model=GenericResponseModel,
)
async def create_rol(rol: RolInsertModel, _=Depends(build_request_context)):
    response: GenericResponseModel = RolService.create_rol(rol=rol)
    return response


@rol_router.get(
    "/list", status_code=http.HTTPStatus.OK, response_model=GenericResponseModel
)
async def list_rol(_=Depends(build_request_context)):
    response: GenericResponseModel = RolService.list_rol()
    return response
