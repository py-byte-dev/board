from fastapi import APIRouter

from backend.presentation.api.routers.banners.route import router as banner_router
from backend.presentation.api.routers.category.route import router as category_router
from backend.presentation.api.routers.city.route import router as city_router
from backend.presentation.api.routers.store.route import router as store_router

router = APIRouter(
    prefix='/api',
)

router.include_router(banner_router)
router.include_router(category_router)
router.include_router(city_router)
router.include_router(store_router)
