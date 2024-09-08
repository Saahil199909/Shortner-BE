from fastapi import APIRouter
from .users import router as users_router
from .generator import router as generators_router
from .redirector import router as redirectors_router
from .user_generated_links import router as user_generated_links_router


api_router = APIRouter()

api_router.include_router(users_router)
api_router.include_router(generators_router)
api_router.include_router(redirectors_router)
api_router.include_router(user_generated_links_router)