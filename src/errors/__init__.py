from fastapi import FastAPI

from . import handlers as h, excaptions as e


def include_errors_handlers(app: FastAPI) -> None:
    errors_handlers = [
        (e.HTTPError, h.http_error_handler),
    ]

    for handler in errors_handlers:
        app.add_exception_handler(*handler)
