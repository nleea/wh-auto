import http
from logger import logger
from utils import build_api_response
from models import GenericResponseModel

from controller import (
    context_set_db_session_rollback,
    context_log_meta,
)
from fastapi import Request


async def pydantic_validation_exception_handler(_: Request, exc):
    context_set_db_session_rollback.set(True)
    logger.error(
        extra=context_log_meta.get(), msg=f"data validation failed {exc.errors()}"
    )
    return build_api_response(
        GenericResponseModel(
            status_code=http.HTTPStatus.BAD_REQUEST, error="Data Validation Failed"
        )
    )


async def fastapi_exception_handler(_: Request, r):
    context_set_db_session_rollback.set(True)
    # logger.error(extra=context_log_meta.get(), msg=r)
    return build_api_response(
        GenericResponseModel(status_code=http.HTTPStatus.BAD_REQUEST, error=str(r))
    )
