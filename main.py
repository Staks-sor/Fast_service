import uvicorn
from fastapi import FastAPI

from src import include_routers
from src.errors import include_errors_handlers
from src.masters.router import router as masters_router
from src.orders.router import router as order_router
from src.works.router import work_router


def get_app() -> FastAPI:
    app = FastAPI(
        title="Auto-service app",
        description="this app is supposed to help auto mechanics do their job",
    )
    app.include_router(work_router)
    app.include_router(masters_router)
    app.include_router(order_router)

    include_routers(app)
    include_errors_handlers(app)

    return app


def main():
    app = get_app()
    uvicorn.run(app)


if __name__ == "__main__":
    main()
