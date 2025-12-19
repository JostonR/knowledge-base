from fastapi import APIRouter
from routers.sources import router as source_router
from routers.insight import router as insight_router
from routers.creator import router as creator_router

api_router = APIRouter(prefix="/api")

api_router.include_router(source_router)
api_router.include_router(insight_router)
api_router.include_router(creator_router)

