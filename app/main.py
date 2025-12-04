from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.db.database import close_db, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}