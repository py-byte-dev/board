from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from backend.application.use_cases.category import GetAllCategoriesInteractor
from backend.presentation.api.routers.category.schemas import CategoriesReponseSchema, CategoryReponseSchema

router = APIRouter(
    prefix='/category',
    route_class=DishkaRoute,
    tags=['category'],
)


@router.get('/all', response_model=CategoriesReponseSchema)
async def get_all_categories(
    interactor: FromDishka[GetAllCategoriesInteractor],
):
    categories = await interactor()

    return CategoriesReponseSchema(
        categories=[CategoryReponseSchema(category=category.title) for category in categories],
    )
