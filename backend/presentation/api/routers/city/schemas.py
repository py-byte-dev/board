from pydantic import BaseModel


class CityResponseSchema(BaseModel):
    city: str


class CitiesResponseSchema(BaseModel):
    cities: list[CityResponseSchema]
