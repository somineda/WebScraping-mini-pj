from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.v1 import router as api_v1_router
from app.core.config import settings
from app.db.database import close_db, init_db
from fastapi.middleware.cors import CORSMiddleware


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

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발용, 프로덕션에서는 특정 도메인만
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}