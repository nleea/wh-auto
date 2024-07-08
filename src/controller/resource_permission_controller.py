import http

from fastapi import APIRouter, Depends

from controller.context_manager import build_request_context
from models.base import GenericResponseModel
from models import ResourcePermissionInsertModel
from service.resource_permission import ResourcePermissionService

resource_permission_router = APIRouter(
    prefix="/v1/resource/permission", tags=["resource-permission"]
)


@resource_permission_router.post(
    "/create",
    status_code=http.HTTPStatus.CREATED,
    response_model=GenericResponseModel,
)
async def create_resource_permission(
    resource_permission: ResourcePermissionInsertModel, _=Depends(build_request_context)
):
    response: GenericResponseModel = (
        ResourcePermissionService.create_resource_permission(
            resource_permission=resource_permission
        )
    )
    return response


@resource_permission_router.get(
    "/{resource_id}",
    status_code=http.HTTPStatus.OK,
    response_model=GenericResponseModel,
)
async def list_resource_permission(resource_id: int, _=Depends(build_request_context)):
    response: GenericResponseModel = (
        ResourcePermissionService.list_permission_by_resource(resource_id)
    )
    return response
