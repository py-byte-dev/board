from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from backend.application.use_cases.city import GetAllCitiesInteractor
from backend.presentation.api.routers.city.schemas import CitiesResponseSchema, CityResponseSchema

router = APIRouter(
    prefix='/city',
    route_class=DishkaRoute,
    tags=['city'],
)


@router.get('/all', response_model=CitiesResponseSchema)
async def get_all_cities(
    interactor: FromDishka[GetAllCitiesInteractor],
):
    cities = await interactor()

    return CitiesResponseSchema(
        cities=[CityResponseSchema(city=city.title) for city in cities],
    )
