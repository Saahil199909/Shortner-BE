from fastapi import APIRouter
from .endpoints import router as redirector_endpoints_router

router = APIRouter()

router.include_router(redirector_endpoints_router, prefix='', tags=["redirector"] )