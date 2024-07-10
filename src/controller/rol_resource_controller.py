import http

from fastapi import APIRouter, Depends

from controller.context_manager import build_request_context
from models.base import GenericResponseModel
from models import RolResourceInsertModel
from service.rol_resource_service import RolResourceService
from utils.helpers import Check

rol_resource_router = APIRouter(prefix="/v1/rol/resource", tags=["rol-resource"])
RESOURCE = "rol_resource"


@rol_resource_router.post(
    "/create",
    status_code=http.HTTPStatus.CREATED,
    response_model=GenericResponseModel,
)
async def create_resource(
    resource: RolResourceInsertModel, _=Depends(build_request_context)
):
    response: GenericResponseModel = RolResourceService.create_rol_resource(
        resource=resource
    )
    return response


@rol_resource_router.get(
    "/by/{rol_id}",
    status_code=http.HTTPStatus.OK,
    response_model=GenericResponseModel,
    dependencies=[Depends(build_request_context), Depends(Check(RESOURCE))],
)
async def rol_resource(
    rol_id: int,
):
    response: GenericResponseModel = RolResourceService.list_resources_by_rol(rol_id)
    return response
