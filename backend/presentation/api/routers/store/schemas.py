from uuid import UUID

from pydantic import BaseModel

from backend.domain.entities.media import MediaType


class StoreResponseSchema(BaseModel):
    id: UUID
    title: str
    description: str
    preview_media_type: MediaType
    main_media_type: MediaType
    main_page_url: str


class StoresReponseSchema(BaseModel):
    total: int
    size: int
    stores: list[StoreResponseSchema]


class StoreResourceResponseSchema(BaseModel):
    title: str
    target_url: str


class StoreDetailsResponseSchema(BaseModel):
    store: StoreResponseSchema
    cities: list[str]
    categories: list[str]
    resources: list[StoreResourceResponseSchema]
