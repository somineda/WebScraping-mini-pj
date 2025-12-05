from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.v1 import router as api_v1_router
from app.core.config import settings
from app.db.database import close_db, init_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import os


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


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def read_root():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
async def dashboard():
    html_path = os.path.join(FRONTEND_DIR, "pages", "dashboard.html")
    return FileResponse(html_path)


@app.get("/diaries", response_class=HTMLResponse, include_in_schema=False)
async def diaries():
    html_path = os.path.join(FRONTEND_DIR, "pages", "diaries.html")
    return FileResponse(html_path)


@app.get("/bookmarks", response_class=HTMLResponse, include_in_schema=False)
async def bookmarks():
    html_path = os.path.join(FRONTEND_DIR, "pages", "bookmarks.html")
    return FileResponse(html_path)

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