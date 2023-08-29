from app.api.routes import models, packages, brands, resolver
from fastapi import APIRouter

router = APIRouter()

router.include_router(models.router, prefix="/models", tags=["models"])
router.include_router(brands.router, prefix="/brands", tags=["brands"])
router.include_router(resolver.router, prefix="/resolver", tags=["resolver"])
router.include_router(packages.router, prefix="/packages", tags=["packages"])
