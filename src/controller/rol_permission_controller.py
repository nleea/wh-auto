import http

from fastapi import APIRouter, Depends

from controller.context_manager import build_request_context
from models.base import GenericResponseModel
from models import RolPermissionInsertModel
from service.rol_permission import RolPermissionService
from utils.helpers import Check

rol_permission_router = APIRouter(prefix="/v1/rol/permission", tags=["rol-permission"])
RESOURCE = "rol_permission"


@rol_permission_router.post(
    "/create",
    status_code=http.HTTPStatus.CREATED,
    response_model=GenericResponseModel,
    dependencies=[Depends(build_request_context), Depends(Check(RESOURCE))],
)
async def create_rol_permission(rol_permission: RolPermissionInsertModel):
    response: GenericResponseModel = RolPermissionService.create_rol_permission(
        rol_permission=rol_permission
    )
    return response


@rol_permission_router.get(
    "/by/{rol_id}",
    status_code=http.HTTPStatus.OK,
    response_model=GenericResponseModel,
    dependencies=[Depends(build_request_context), Depends(Check(RESOURCE))],
)
async def list_rol_permission(rol_id: int):
    response: GenericResponseModel = RolPermissionService.list_permission_by_rol(rol_id)
    return response
