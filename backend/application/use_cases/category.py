from collections.abc import Collection
from typing import Protocol
from uuid import UUID

from backend.application import interfaces
from backend.domain.entities.category import Category, CategorySelection


class GetCategoryInteractor:
    def __init__(
        self,
        reader: interfaces.CategoryReader,
    ):
        self._reader = reader

    async def __call__(self, category_id: UUID) -> Category:
        return await self._reader.get_by_id(category_id=category_id)


class GetAllCategoriesInteractor:
    def __init__(
        self,
        reader: interfaces.CategoryReader,
    ):
        self._reader = reader

    async def __call__(self) -> Collection[Category]:
        return await self._reader.get_all()


class GetStoreCategoriesInteractor:
    def __init__(
        self,
        reader: interfaces.CategoryReader,
    ):
        self._reader = reader

    async def __call__(self, store_id: UUID) -> Collection[CategorySelection]:
        return await self._reader.get_store_category_selection(store_id=store_id)


class SaveCategoriesInteractor:
    def __init__(
        self,
        saver: interfaces.CategorySaver,
        uuid_generator: interfaces.UUIDGenerator,
    ):
        self._saver = saver
        self._uuid_generator = uuid_generator

    async def __call__(self, titles: str) -> None:
        categories = [Category(id=self._uuid_generator(), title=title.strip()) for title in titles.split('\n')]

        await self._saver.save(categories=categories)


class DeleteCategoryManager(interfaces.CategoryReader, interfaces.CategoryDeleter, Protocol): ...


class DeleteCategoryInteractor:
    def __init__(
        self,
        deleter: DeleteCategoryManager,
    ):
        self._deleter = deleter

    async def __call__(self, category_id: UUID) -> None:
        category = await self._deleter.get_by_id(category_id=category_id)
        await self._deleter.delete(category=category)

        return await self._deleter.get_all()
