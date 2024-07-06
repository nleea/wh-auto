import http
import json
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


async def sql_exception_handler(_: Request, exc):
    context_set_db_session_rollback.set(True)
    logger.error(
        extra=context_log_meta.get(),
        msg=f"sql exception occurred error: {str(exc.args)} statement : {exc.statement}",
    )
    return build_api_response(
        GenericResponseModel(
            status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR, error="Data Source Error"
        )
    )


async def sql_data_exception_handler(_: Request, exc):
    context_set_db_session_rollback.set(True)
    logger.error(
        extra=context_log_meta.get(),
        msg=f"sql data exception occurred error: {str(exc.args)} statement : {exc.statement}",
    )
    return build_api_response(
        GenericResponseModel(
            status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
            error="Data Error for data provided",
        )
    )


async def application_exception_handler(_: Request, exc):
    context_set_db_session_rollback.set(True)
    logger.error(
        extra=context_log_meta.get(),
        msg=f"application exception occurred error: {json.loads(str(exc))}",
    )
    return build_api_response(
        GenericResponseModel(status_code=exc.status_code, error=exc.message)
    )


async def sql_integrity_exception_handler(_: Request, exc):
    context_set_db_session_rollback.set(True)
    logger.error(
        extra=context_log_meta.get(),
        msg=f"sql integrity exception occurred error: {str(exc.args)} statement : {exc.statement}",
    )
    return build_api_response(
        GenericResponseModel(
            status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
            error="Integrity Error for data provided",
        )
    )
