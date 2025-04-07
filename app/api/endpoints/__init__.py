from .search import router as search_router
from .filesystem import router as filesystem_router
from .tools import router as tools_router
from .health import router as health_router
from .claude import router as claude_router
from .prompts import router as prompts_router
from .logs import router as logs_router

__all__ = [
    'search_router',
    'filesystem_router',
    'tools_router',
    'health_router',
    'claude_router',
    'prompts_router',
    'logs_router'
] 