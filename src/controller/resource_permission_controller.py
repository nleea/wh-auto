import http

from fastapi import APIRouter, Depends

from controller.context_manager import build_request_context
from models.base import GenericResponseModel
from models import ResourcePermissionInsertModel
from service.resource_permission import ResourcePermissionService
from utils.helpers import Check

resource_permission_router = APIRouter(
    prefix="/v1/resource/permission", tags=["resource-permission"]
)

RESOURCE = "resource_permission"


@resource_permission_router.post(
    "/create",
    status_code=http.HTTPStatus.CREATED,
    response_model=GenericResponseModel,
    dependencies=[Depends(build_request_context), Depends(Check(RESOURCE))],
)
async def create_resource_permission(
    resource_permission: ResourcePermissionInsertModel,
):
    response: GenericResponseModel = (
        ResourcePermissionService.create_resource_permission(
            resource_permission=resource_permission
        )
    )
    return response


@resource_permission_router.get(
    "/by/{resource_id}",
    status_code=http.HTTPStatus.OK,
    response_model=GenericResponseModel,
    dependencies=[Depends(build_request_context), Depends(Check(RESOURCE))],
)
async def list_resource_permission(resource_id: int):
    response: GenericResponseModel = (
        ResourcePermissionService.list_permission_by_resource(resource_id)
    )
    return response
