from abc import abstractmethod
from collections.abc import Collection
from typing import Protocol
from uuid import UUID

from backend.domain.entities.media import Media, StoreMediaName
from backend.domain.entities.store import Store, StoreDetails


class StoreReader(Protocol):
    @abstractmethod
    async def get_by_id(self, store_id: UUID) -> Store: ...

    @abstractmethod
    async def get_with_relations(self, store_id: UUID) -> StoreDetails: ...

    @abstractmethod
    async def get_all(self) -> Collection[Store]: ...

    @abstractmethod
    async def get_by_filter(
        self,
        store_title: str | None,
        city_title: str | None,
        categories_title: Collection[str] | None,
    ) -> Collection[Store]: ...


class StoreSaver(Protocol):
    @abstractmethod
    async def save(
        self,
        store: Store,
        preview_media_pc: Media,
        preview_media_mobile: Media,
        main_media_pc: Media,
        main_media_mobile: Media,
        bucket: str,
    ) -> None: ...


class StoreUpdater(Protocol):
    @abstractmethod
    async def update(self, store: Store) -> None: ...

    @abstractmethod
    async def update_media(self, store: Store, media: Media, media_name: StoreMediaName, bucket: str) -> None: ...


class StoreDeleter(Protocol):
    @abstractmethod
    async def delete(self, store: Store) -> None: ...
