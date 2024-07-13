import http

from fastapi import APIRouter, Depends, Request

from controller.context_manager import build_request_context
from models.base import GenericResponseModel
from models import ResourceInsertModel
from service.resource_service import ResourceService
from utils.helpers import Check
from config.limiter import limiter

resource_router = APIRouter(prefix="/v1/resource", tags=["resource"])
RESOURCE = "resources"


@resource_router.post(
    "/create",
    status_code=http.HTTPStatus.CREATED,
    response_model=GenericResponseModel,
    dependencies=[Depends(build_request_context), Depends(Check(RESOURCE, True))],
)
@limiter.limit("5/minutes")
async def create_resource(
    request: Request, resource: ResourceInsertModel, _=Depends(build_request_context)
):
    response: GenericResponseModel = ResourceService.create_resource(resource=resource)
    return response


@resource_router.get(
    "/list",
    status_code=http.HTTPStatus.OK,
    response_model=GenericResponseModel,
    dependencies=[Depends(build_request_context), Depends(Check(RESOURCE, True))],
)
@limiter.limit("5/minutes")
async def list_resources(request: Request):
    response: GenericResponseModel = ResourceService.list_resources()
    return response
