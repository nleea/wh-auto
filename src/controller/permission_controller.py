import http

from fastapi import APIRouter, Depends

from controller.context_manager import build_request_context
from models.base import GenericResponseModel
from models import PermissionsInsertModel
from service.permission_service import PermissionService

permissions_router = APIRouter(prefix="/v1/permissions", tags=["permissions"])


@permissions_router.post(
    "/create",
    status_code=http.HTTPStatus.CREATED,
    response_model=GenericResponseModel,
)
async def create_resource(
    permission: PermissionsInsertModel, _=Depends(build_request_context)
):
    response: GenericResponseModel = PermissionService.create_permission(permission=permission)
    return response


@permissions_router.get(
    "/list", status_code=http.HTTPStatus.OK, response_model=GenericResponseModel
)
async def list_resources(_=Depends(build_request_context)):
    response: GenericResponseModel = PermissionService.list_permissions()
    return response
