from fastapi import FastAPI
from fastapi.exceptions import FastAPIError
import uvicorn
from exception.exception import (
    pydantic_validation_exception_handler,
    fastapi_exception_handler,
)
from pydantic import ValidationError
from controller.user import user_router
from controller.rol import rol_router
from controller.gender import gender_router

app = FastAPI()


@app.get("/")
def main():
    return "Ok"


""" Routes """
app.include_router(user_router, prefix="")
app.include_router(rol_router, prefix="")
app.include_router(gender_router, prefix="")

""" Exceptions  """
app.add_exception_handler(ValidationError, pydantic_validation_exception_handler)
app.add_exception_handler(FastAPIError, fastapi_exception_handler)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_excludes=["log/*", "log/**"],
    )
