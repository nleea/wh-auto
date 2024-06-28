from typing import Any
from utils import build_api_response
from starlette.middleware.base import BaseHTTPMiddleware
import json


class ResponseMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request, call_next) -> Any:
        # print("before call_next")
        response = await call_next(request)
        # print("before body", response)
        body = [section async for section in response.body_iterator]
        # print("body", body)
        response_body = json.loads(b"".join(body))
        return build_api_response(response_body)
