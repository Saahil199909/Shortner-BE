from fastapi import APIRouter
from .endpoints import router as user_endpoints_router


router = APIRouter()

router.include_router(user_endpoints_router, prefix='/users', tags=["users"] )