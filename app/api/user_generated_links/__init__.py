from fastapi import APIRouter
from .endpoints import router as user_generated_links_endpoints_router

router = APIRouter()

router.include_router(user_generated_links_endpoints_router, prefix='/user_generated_links', tags=["user generated links"] )