from abc import abstractmethod
from collections.abc import Collection
from typing import Protocol
from uuid import UUID

from backend.domain.entities.banner import Banner
from backend.domain.entities.media import BannerMediaName, Media


class BannerReader(Protocol):
    @abstractmethod
    async def get_by_id(self, banner_id: UUID) -> Banner: ...

    @abstractmethod
    async def get_all(self) -> Collection[Banner]: ...


class BannerSaver(Protocol):
    @abstractmethod
    async def save(self, banner: Banner, pc_media: Media, mobile_media: Media, bucket: str) -> None: ...


class BannerUpdater(Protocol):
    @abstractmethod
    async def update(self, banner: Banner) -> None: ...

    @abstractmethod
    async def update_media(self, banner: Banner, media: Media, media_name: BannerMediaName, bucket: str) -> None: ...


class BannerDeleter(Protocol):
    @abstractmethod
    async def delete(self, banner: Banner) -> None: ...
