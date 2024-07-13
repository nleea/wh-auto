import http

from fastapi import APIRouter, Depends, Request

from controller.context_manager import build_request_context
from models.base import GenericResponseModel
from models.base_model import RolInsertModel
from service.rol_service import RolService
from utils.helpers import Check
from config.limiter import limiter

rol_router = APIRouter(prefix="/v1/rol", tags=["rol"])

RESOURCE = "rol"


@rol_router.post(
    "/create",
    status_code=http.HTTPStatus.CREATED,
    response_model=GenericResponseModel,
    dependencies=[Depends(build_request_context), Depends(Check(RESOURCE, True))],
)
@limiter.limit("5/minutes")
async def create_rol(request: Request, rol: RolInsertModel):
    response: GenericResponseModel = RolService.create_rol(rol=rol)
    return response


@rol_router.get(
    "/list",
    status_code=http.HTTPStatus.OK,
    response_model=GenericResponseModel,
    dependencies=[Depends(build_request_context), Depends(Check(RESOURCE, True))],
)
@limiter.limit("5/minutes")
async def list_rol(request: Request):
    response: GenericResponseModel = RolService.list_rol()
    return response
