from fastapi import Request
from fastapi.responses import JSONResponse

from .excaptions import ApplicationException, HTTPError


def http_error_handler(request: Request, exc: ApplicationException):
    return JSONResponse(status_code=exc.status_code, content=exc.message_text)
