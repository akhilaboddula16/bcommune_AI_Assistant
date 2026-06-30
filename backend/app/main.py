from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.db_test import router as db_test_router
from app.core.config import get_settings
from app.core.logging_config import setup_logging
from app.api.routes.auth import router as auth_router
from app.api.routes.admin import router as admin_router
from app.api.routes.documents import router as documents_router
from app.api.routes.search import router as search_router


setup_logging()
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(db_test_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(documents_router)
app.include_router(search_router)

@app.get("/")
def root():
    return {
        "message": "Bcommune AI Assistant Backend is running",
    }