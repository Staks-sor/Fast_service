import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src import include_routers
from src.errors import excaptions, handlers
from src.masters.router import router as masters_router
from src.orders.router import router as order_router
from src.works.router import work_router

print("gfgfgf")
def get_app() -> FastAPI:
    app = FastAPI(
        title="Auto-service app",
        description="this app is supposed to help auto mechanics do their job",
    )

    app.include_router(work_router)
    app.include_router(masters_router)
    app.include_router(order_router)

    @app.exception_handler(excaptions.ApplicationException)
    async def handle_application_exception(
        request: Request, exc: excaptions.ApplicationException
    ):
        return JSONResponse(
            status_code=exc.status_code, content={"error": exc.message}
        )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    include_routers(app)

    return app


def main():
    app = get_app()
    uvicorn.run(app)


if __name__ == "__main__":
    main()
