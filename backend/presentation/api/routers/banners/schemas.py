from uuid import UUID

from pydantic import BaseModel

from backend.domain.entities.media import MediaType


class BannerReponseSchema(BaseModel):
    id: UUID
    media_type: MediaType
    target_url: str
    display_priority: int


class BannersReponseSchema(BaseModel):
    banners: list[BannerReponseSchema]
