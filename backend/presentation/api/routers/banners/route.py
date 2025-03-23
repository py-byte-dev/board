from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from backend.application.use_cases.banner import GetBannersInteractor
from backend.presentation.api.routers.banners.schemas import BannerReponseSchema, BannersReponseSchema

router = APIRouter(
    prefix='/banner',
    route_class=DishkaRoute,
    tags=['banner'],
)


@router.get('/all', response_model=BannersReponseSchema)
async def get_all_banners(
    interactor: FromDishka[GetBannersInteractor],
):
    banners = await interactor()

    return BannersReponseSchema(
        banners=[
            BannerReponseSchema(
                id=banner.id,
                media_type=banner.media_type,
                target_url=banner.target_url,
                display_priority=banner.display_priority
            )
            for banner in banners
        ]
    )
