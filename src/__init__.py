from fastapi import FastAPI, APIRouter

from .auth import auth_router


def include_routers(app: FastAPI) -> None:
    routers: list[APIRouter] = [
        auth_router
    ]

    for router in routers:
        app.include_router(router)
