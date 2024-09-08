from fastapi import APIRouter
from .endpoints import router as generator_endpoints_router


router = APIRouter()

router.include_router(generator_endpoints_router, prefix='/generator', tags=["generator"] )