from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from src import include_routers
from src.errors import include_errors_handlers


def get_app() -> FastAPI:
    app = FastAPI(
        title="Auto-service app",
        description="this app is supposed to help auto mechanics do their job",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    include_routers(app)
    include_errors_handlers(app)

    return app


def main():
    app = get_app()
    uvicorn.run(app)


if __name__ == "__main__":
    main()
