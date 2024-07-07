from typing import Any
from utils import build_api_response
from starlette.middleware.base import BaseHTTPMiddleware
import json
from fastapi.responses import JSONResponse


class ResponseMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request, call_next) -> Any:
        try:
            response = await call_next(request)
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"message": f"An internal server error occurred, {e}"},
            )
        body = [section async for section in response.body_iterator]
        response_body = json.loads(b"".join(body))

        return build_api_response(response_body)
