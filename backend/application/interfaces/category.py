from abc import abstractmethod
from collections.abc import Collection
from typing import Protocol
from uuid import UUID

from backend.domain.entities.category import Category, CategorySelection


class CategoryReader(Protocol):
    @abstractmethod
    async def get_by_id(self, category_id: UUID) -> Category: ...

    @abstractmethod
    async def get_all(self) -> Collection[Category]: ...

    @abstractmethod
    async def get_store_category_selection(self, store_id: UUID) -> Collection[CategorySelection]: ...


class CategorySaver(Protocol):
    @abstractmethod
    async def save(self, categories: Collection[Category]) -> None: ...


class CategoryUpdater(Protocol):
    @abstractmethod
    async def update(self, category: Category) -> None: ...


class CategoryDeleter(Protocol):
    @abstractmethod
    async def delete(self, category: Category) -> None: ...
