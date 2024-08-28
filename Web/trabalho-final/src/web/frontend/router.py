from fastapi.routing import APIRouter

from src.web.frontend import core

frontend_router = APIRouter()
frontend_router.include_router(core.router)
