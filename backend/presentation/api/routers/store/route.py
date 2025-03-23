from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from backend.application.use_cases.store import (
    GetAllStoresInteractor,
    GetStoreDetailsInteractor,
    GetStoresByFilterInteractor,
)
from backend.presentation.api.routers.store.schemas import (
    StoreDetailsResponseSchema,
    StoreResourceResponseSchema,
    StoreResponseSchema,
    StoresReponseSchema,
)

router = APIRouter(
    prefix='/store',
    route_class=DishkaRoute,
    tags=['store'],
)


@router.get('/all', response_model=StoresReponseSchema)
async def get_all_stores(
    page: int,
    page_size: int,
    interactor: FromDishka[GetAllStoresInteractor],
):
    stores = await interactor(page=page, page_size=page_size)

    return StoresReponseSchema(
        total=stores.total,
        size=stores.size,
        stores=[
            StoreResponseSchema(
                id=store.id,
                title=store.title,
                description=store.description,
                preview_media_type=store.preview_media_type,
                main_media_type=store.main_media_type,
                main_page_url=store.main_page_url,
            )
            for store in stores.items
        ],
    )


@router.get('/by-id', response_model=StoreDetailsResponseSchema)
async def get_store_details(
    store_id: UUID,
    interactor: FromDishka[GetStoreDetailsInteractor],
):
    details = await interactor(store_id=store_id)
    return StoreDetailsResponseSchema(
        store=StoreResponseSchema(
            id=details.store.id,
            title=details.store.title,
            description=details.store.description,
            preview_media_type=details.store.preview_media_type,
            main_media_type=details.store.main_media_type,
            main_page_url=details.store.main_page_url,
        ),
        cities=[city.title for city in details.cities],
        categories=[category.title for category in details.categories],
        resources=[
            StoreResourceResponseSchema(
                title=resource.title,
                target_url=resource.target_url,
            )
            for resource in details.resources
        ],
    )


@router.get('/by-filters', response_model=StoresReponseSchema)
async def get_stors_by_filters(
    interactor: FromDishka[GetStoresByFilterInteractor],
    page: int,
    page_size: int,
    store_title: str | None = None,
    city_title: str | None = None,
    categories_title: str | None = None,
):
    print(city_title)
    stores = await interactor(
        page=page,
        page_size=page_size,
        store_title=store_title,
        city_title=city_title,
        categories_title=categories_title,
    )

    return StoresReponseSchema(
        total=stores.total,
        size=stores.size,
        stores=[
            StoreResponseSchema(
                id=store.id,
                title=store.title,
                description=store.description,
                preview_media_type=store.preview_media_type,
                main_media_type=store.main_media_type,
                main_page_url=store.main_page_url,
            )
            for store in stores.items
        ],
    )
