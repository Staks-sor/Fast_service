from fastapi import Request
from fastapi.responses import JSONResponse

from .excaptions import HTTPError


async def http_error_handler(request: Request, exc: HTTPError):
    content = {"errors": exc.errors, "detail": exc.detail}

    return JSONResponse(status_code=exc.status_code, content=content)
