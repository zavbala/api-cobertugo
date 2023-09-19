from fastapi import APIRouter

from app.api.routes import brands, models, quotes, refine

router = APIRouter()

router.include_router(models.router, prefix="/models", tags=["models"])
router.include_router(brands.router, prefix="/brands", tags=["brands"])
router.include_router(quotes.router, prefix="/quotes", tags=["quotes"])
router.include_router(refine.router, prefix="/refine", tags=["refine"])
