from fastapi import FastAPI
from src.auth.router import router as auth_router
import uvicorn

app = FastAPI(
    title="Auto-sevice app",
    description="this app is supposed to help auto mechanics do their job",
)

app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app)
