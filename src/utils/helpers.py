import http
import uuid

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from logger import logger
from models.base import GenericResponseModel
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated, Any
from fastapi import Depends, Request
from utils.jwt_handler import JWTHandler
from sqlalchemy import and_

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def build_api_response(generic_response: GenericResponseModel) -> JSONResponse:
    from controller.context_manager import context_api_id, context_log_meta
    
    if type(generic_response) == GenericResponseModel:
        generic_response = {
            "api_id": generic_response.api_id,
            "status_code": generic_response.status_code,
            "error": generic_response.error,
            "message": generic_response.message,
            "data": generic_response.data
        }
    
    try:    
        if "detail" in generic_response:
            generic_response["api_id"] = (
                context_api_id.get() if context_api_id.get() else str(uuid.uuid4())
            )
            generic_response["error"] =  generic_response["detail"]
            generic_response["message"] = "Type validation fail"
            del generic_response["detail"]
            response_json = jsonable_encoder(generic_response)
            res = JSONResponse(
            status_code=404, content=response_json
            )
            
            return res

        if "api_id" not in generic_response or not generic_response["api_id"]:
            generic_response["api_id"] = (
                context_api_id.get() if context_api_id.get() else str(uuid.uuid4())
            )

        if "status_code" not in generic_response or not generic_response["status_code"]:
            generic_response["status_code"] = (
                http.HTTPStatus.OK
                if not generic_response["error"]
                else http.HTTPStatus.UNPROCESSABLE_ENTITY
            )

        response_json = jsonable_encoder(generic_response)
        res = JSONResponse(
            status_code=generic_response["status_code"], content=response_json
        )
        logger.info(
            extra=context_log_meta.get(),
            msg="build_api_response: Generated Response with status_code:"
            + f"{generic_response["status_code"]}",
        )
        return res
    except Exception as e:
        logger.error(
            extra=context_log_meta.get(),
            msg=f"exception in build_api_response error : {e}",
        )
        return JSONResponse(
            status_code=generic_response.status_code, content=generic_response.error
        )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    JWTHandler.decode_access_token(token)

class Check:

    def __init__(self, resource) -> None:
        self.resource = resource    

    def get_role_with_permissions_and_resources(self, user_rol: str, permission_name: str,resource_name: str ):

            from controller.context_manager import get_db_session
            from data_adapter.base_tables import Rol
            from data_adapter.resources import RolResources
            from data_adapter.permission import RolPermission
            
            db = get_db_session()

            rol = db.query(Rol).filter(
                and_(
                Rol.name_rol == user_rol,
                Rol.rol_permissions.any(RolPermission.permission.has(name=permission_name)),
                Rol.rol_resources.any(RolResources.resource.has(name=resource_name))
            )
                ).one_or_none()

            return rol is not None
    
    def __call__(self, request: Request) -> Any:
        from utils.exceptions import AppException
        try:
            from controller.context_manager import context_actor_user_data

            user_context = context_actor_user_data.get()

            if user_context.role == "admin":
                return

            required_permission = request.get("path").split("/")[-1]

            if request.get("path_params"):
                required_permission = request.get("path").split("/")[-2]

            has_permission_and_resource = self.get_role_with_permissions_and_resources(
                user_rol=user_context.role, 
                permission_name=required_permission, 
                resource_name=self.resource
            )

            if not has_permission_and_resource:
                raise AppException(401,"you don't have the permission for do this action")
        except AppException:
            raise AppException(401,"you don't have the permission for do this action")
        
