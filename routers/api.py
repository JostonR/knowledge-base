from fastapi import APIRouter
from routers.sources import router as source_router

api_router = APIRouter(prefix="/api")

api_router.include_router(source_router)

