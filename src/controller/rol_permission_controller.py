import http

from fastapi import APIRouter, Depends

from controller.context_manager import build_request_context
from models.base import GenericResponseModel
from models import RolPermissionInsertModel
from service.rol_permission import RolPermissionService

rol_permission_router = APIRouter(prefix="/v1/rol/permission", tags=["rol-permission"])


@rol_permission_router.post(
    "/create",
    status_code=http.HTTPStatus.CREATED,
    response_model=GenericResponseModel,
)
async def create_rol_permission(
    rol_permission: RolPermissionInsertModel, _=Depends(build_request_context)
):
    response: GenericResponseModel = RolPermissionService.create_rol_permission(
        rol_permission=rol_permission
    )
    return response


@rol_permission_router.get(
    "/{rol_id}", status_code=http.HTTPStatus.OK, response_model=GenericResponseModel
)
async def list_rol_permission(rol_id: int, _=Depends(build_request_context)):
    response: GenericResponseModel = RolPermissionService.list_permission_by_rol(rol_id)
    return response