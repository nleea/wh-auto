import http

from fastapi import APIRouter, Depends

from controller.context_manager import build_request_context
from models.base import GenericResponseModel
from models import ResourceInsertModel
from service.resource_service import ResourceService

resource_router = APIRouter(prefix="/v1/resource", tags=["resource"])


@resource_router.post(
    "/create",
    status_code=http.HTTPStatus.CREATED,
    response_model=GenericResponseModel,
)
async def create_resource(
    resource: ResourceInsertModel, _=Depends(build_request_context)
):
    response: GenericResponseModel = ResourceService.create_resource(resource=resource)
    return response


@resource_router.get(
    "/list", status_code=http.HTTPStatus.OK, response_model=GenericResponseModel
)
async def list_resources(_=Depends(build_request_context)):
    response: GenericResponseModel = ResourceService.list_resources()
    return response
