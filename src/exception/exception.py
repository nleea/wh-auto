import http
import json
from logger import logger

from controller import (
    context_set_db_session_rollback,
    context_log_meta,
)
from fastapi import Request
from fastapi.responses import JSONResponse


async def pydantic_validation_exception_handler(_: Request, exc):
    context_set_db_session_rollback.set(True)
    logger.error(
        extra=context_log_meta.get(), msg=f"data validation failed {exc.errors()}"
    )
    return JSONResponse(
        status_code=http.HTTPStatus.BAD_REQUEST,
        content={"status_code": 400, "error": "Data Validation Failed"},
    )


async def fastapi_exception_handler(_: Request, exc):
    context_set_db_session_rollback.set(True)
    logger.error(extra=context_log_meta.get(), msg=exc)
    return JSONResponse(
        status_code=400, content={"status_code": 400, "error": str(exc)}
    )


async def sql_exception_handler(_: Request, exc):
    context_set_db_session_rollback.set(True)
    logger.error(
        extra=context_log_meta.get(),
        msg=f"sql exception occurred error: {str(exc.args)} statement",
    )
    return JSONResponse(
        status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
        content={
            "status_code": http.HTTPStatus.INTERNAL_SERVER_ERROR,
            "error": "Data Source Error",
        },
    )


async def sql_data_exception_handler(_: Request, exc):
    context_set_db_session_rollback.set(True)
    logger.error(
        extra=context_log_meta.get(),
        msg=f"sql data exception occurred error: {str(exc.args)} statement ",
    )
    return JSONResponse(
        status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
        content={
            "status_code": http.HTTPStatus.INTERNAL_SERVER_ERROR,
            "error": "Data Error for data provided",
        },
    )


async def application_exception_handler(_: Request, exc):
    context_set_db_session_rollback.set(True)
    logger.error(
        extra=context_log_meta.get(),
        msg=f"application exception occurred error: {json.loads(str(exc))}",
    )

    return JSONResponse(
        status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
        content={"status_code": exc.status_code, "error": exc.message},
    )


async def sql_integrity_exception_handler(_: Request, exc):
    context_set_db_session_rollback.set(True)
    logger.error(
        extra=context_log_meta.get(),
        msg=f"sql integrity exception occurred error: {str(exc.args)} statement ",
    )

    return JSONResponse(
        status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
        content={
            "status_code": exc.status_code,
            "error": "Integrity Error for data provided",
        },
    )


async def auth_exception_handlre(_: Request, exc):
    context_set_db_session_rollback.set(True)
    logger.error(
        extra=context_log_meta.get(),
        msg="Auth Exception",
    )
    return JSONResponse(
        status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
        content={
            "status_code": http.HTTPStatus.UNAUTHORIZED,
            "error": "Auth exception",
        },
    )
