from fastapi import FastAPI
from fastapi.exceptions import FastAPIError
from sqlalchemy.exc import ProgrammingError, DataError, IntegrityError
import uvicorn
from exception import (
    pydantic_validation_exception_handler,
    fastapi_exception_handler,
    sql_integrity_exception_handler,
    sql_data_exception_handler,
    application_exception_handler,
    sql_exception_handler,
)
from utils.exceptions import AppException
from pydantic import ValidationError
from controller import (
    rol_router,
    gender_router,
    user_router,
    auth_router,
    resource_router,
    rol_resource_router,
)
from middleware import ResponseMiddleware

app = FastAPI()


@app.get("/")
def main():
    return "Ok"


""" Routes """
app.include_router(user_router, prefix="")
app.include_router(rol_router, prefix="")
app.include_router(gender_router, prefix="")
app.include_router(auth_router, prefix="")
app.include_router(resource_router, prefix="")
app.include_router(rol_resource_router, prefix="")


""" Exceptions  """
app.add_exception_handler(ValidationError, pydantic_validation_exception_handler)
app.add_exception_handler(FastAPIError, fastapi_exception_handler)
app.add_exception_handler(ProgrammingError, sql_exception_handler)
app.add_exception_handler(DataError, sql_data_exception_handler)
app.add_exception_handler(AppException, application_exception_handler)
app.add_exception_handler(AppException, sql_integrity_exception_handler)


""" Middlewares """
app.add_middleware(ResponseMiddleware)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_excludes=["log/*", "log/**"],
    )
