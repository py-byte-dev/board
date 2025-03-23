from pydantic import BaseModel


class CategoryReponseSchema(BaseModel):
    category: str


class CategoriesReponseSchema(BaseModel):
    categories: list[CategoryReponseSchema]
