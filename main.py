from fastapi import FastAPI
from src.auth.router import router as auth_router

app = FastAPI(
    title="Auto-service app",
    description="this app is supposed to help auto mechanics do their job",
)

app.include_router(auth_router)
