from fastapi import APIRouter
from .search import router as search_router
from .filesystem import router as filesystem_router
from .tools import router as tools_router
from .health import router as health_router
from .claude import router as claude_router
from .prompts import router as prompts_router
from .logs import router as logs_router
from .resources import router as resources_router

router = APIRouter()

router.include_router(search_router)
router.include_router(filesystem_router)
router.include_router(tools_router)
router.include_router(health_router)
router.include_router(claude_router)
router.include_router(prompts_router)
router.include_router(logs_router)
router.include_router(resources_router)

__all__ = [
    "search_router",
    "filesystem_router",
    "tools_router",
    "health_router",
    "claude_router",
    "prompts_router",
    "logs_router",
    "resources_router"
] 