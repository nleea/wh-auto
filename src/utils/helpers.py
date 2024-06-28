import http
import uuid

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from logger import logger
from models.base import GenericResponseModel


def build_api_response(generic_response: GenericResponseModel) -> JSONResponse:
    from controller import context_api_id, context_log_meta
    
    
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

        if "api_id" not in generic_response and not generic_response["api_id"]:
            generic_response["api_id"] = (
                context_api_id.get() if context_api_id.get() else str(uuid.uuid4())
            )

        if "status_code" not in generic_response and not generic_response["status_code"]:
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
