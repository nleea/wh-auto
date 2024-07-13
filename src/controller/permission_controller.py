import http

from fastapi import APIRouter, Depends, Request

from controller.context_manager import build_request_context
from models.base import GenericResponseModel
from models import PermissionsInsertModel
from service.permission_service import PermissionService
from utils.helpers import Check
from config.limiter import limiter

permissions_router = APIRouter(prefix="/v1/permissions", tags=["permissions"])
RESOURCE = "permission"


@permissions_router.post(
    "/create",
    status_code=http.HTTPStatus.CREATED,
    response_model=GenericResponseModel,
    dependencies=[Depends(build_request_context), Depends(Check(RESOURCE, True))],
)
@limiter.limit("5/minutes")
async def create_resource(request: Request, permission: PermissionsInsertModel):
    response: GenericResponseModel = PermissionService.create_permission(
        permission=permission
    )
    return response


@permissions_router.get(
    "/list",
    status_code=http.HTTPStatus.OK,
    response_model=GenericResponseModel,
    dependencies=[Depends(build_request_context), Depends(Check(RESOURCE, True))],
)
@limiter.limit("5/minutes")
async def list_resources(request: Request):
    response: GenericResponseModel = PermissionService.list_permissions()
    return response
