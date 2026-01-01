from fastapi import APIRouter
from routers.sources import router as source_router
from routers.insight import router as insight_router
from routers.creator import router as creator_router
from routers.bible_references import router as bibleref_router
from routers.debug import router as debug
from routers.quote import router as quote

api_router = APIRouter(prefix="/api")

api_router.include_router(source_router)
api_router.include_router(insight_router)
api_router.include_router(creator_router)
api_router.include_router(bibleref_router)
api_router.include_router(debug)
api_router.include_router(quote)
