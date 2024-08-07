from fastapi import FastAPI, Depends
from fastapi.exceptions import FastAPIError
from sqlalchemy.exc import ProgrammingError, DataError
import uvicorn
from exception import (
    pydantic_validation_exception_handler,
    fastapi_exception_handler,
    sql_data_exception_handler,
    application_exception_handler,
    sql_exception_handler,
    auth_exception_handlre,
)
from utils.exceptions import AppException, AuthException
from pydantic import ValidationError
from controller import (
    rol_router,
    gender_router,
    user_router,
    auth_router,
    resource_router,
    rol_resource_router,
    permissions_router,
    rol_permission_router,
    resource_permission_router
)
from middleware import ResponseMiddleware
from utils.helpers import get_current_user
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from config.settings import origins
from config.limiter import limiter
from slowapi.middleware import SlowAPIMiddleware


app = FastAPI(root_path="/api/v1")
app.state.limiter = limiter


""" Routes """
app.include_router(user_router, prefix="", dependencies=[Depends(get_current_user)])
app.include_router(rol_router, prefix="", dependencies=[Depends(get_current_user)])
app.include_router(gender_router, prefix="", dependencies=[Depends(get_current_user)])
app.include_router(auth_router, prefix="")
app.include_router(resource_router, prefix="", dependencies=[Depends(get_current_user)])
app.include_router(rol_resource_router, prefix="", dependencies=[Depends(get_current_user)])
app.include_router(permissions_router, prefix="", dependencies=[Depends(get_current_user)])
app.include_router(rol_permission_router, prefix="", dependencies=[Depends(get_current_user)])
app.include_router(resource_permission_router, prefix="", dependencies=[Depends(get_current_user)])


""" Exceptions  """
app.add_exception_handler(AuthException, auth_exception_handlre)
app.add_exception_handler(ValidationError, pydantic_validation_exception_handler)
app.add_exception_handler(FastAPIError, fastapi_exception_handler)
app.add_exception_handler(ProgrammingError, sql_exception_handler)
app.add_exception_handler(DataError, sql_data_exception_handler)
app.add_exception_handler(AppException, application_exception_handler)

""" Middlewares """
app.add_middleware(ResponseMiddleware)
app.middleware(GZipMiddleware(app,minimum_size=1000))
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SlowAPIMiddleware)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_excludes=["log/*", "log/**"],
    )
