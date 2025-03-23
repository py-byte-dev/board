from abc import abstractmethod
from collections.abc import Collection
from typing import Protocol
from uuid import UUID

from backend.domain.entities.store_category import StoreCategory


class StoreCategoryReader(Protocol):
    @abstractmethod
    async def relationship_exists(self, store_id: UUID, category_id: UUID) -> bool: ...

    @abstractmethod
    async def get_by_store_category_ids(self, store_id: UUID, category_id: UUID) -> StoreCategory: ...

    @abstractmethod
    async def get_by_id(self, store_category_id: UUID) -> StoreCategory: ...


class StoreCategorySaver(Protocol):
    @abstractmethod
    async def save(self, store_category: StoreCategory) -> None: ...

    @abstractmethod
    async def save_many(self, store_categories: Collection[StoreCategory]) -> None: ...


class StoreCategoryDeleter(Protocol):
    @abstractmethod
    async def delete(self, store_category: StoreCategory) -> None: ...
