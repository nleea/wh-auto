from typing import Any
from utils import build_api_response
from starlette.middleware.base import BaseHTTPMiddleware
import json


class ResponseMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request, call_next) -> Any:
        response = await call_next(request)
        body = [section async for section in response.body_iterator]
        response_body = json.loads(b"".join(body))
        
        if response.status_code in [400,404,500]:
            return build_api_response(
                {"body": response_body, "status_code": response.status_code}
            )

        return build_api_response(response_body)