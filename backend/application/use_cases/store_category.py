from collections.abc import Collection
from typing import Protocol
from uuid import UUID

from backend.application import interfaces
from backend.domain.entities.category import CategorySelection
from backend.domain.entities.store_category import StoreCategory


class AddStoreCategoryManager(interfaces.StoreCategoryReader, interfaces.StoreCategorySaver, Protocol): ...


class AddStoreCategoryInteractor:
    def __init__(
        self,
        saver: AddStoreCategoryManager,
        category_reader: interfaces.CategoryReader,
        uuid_generator: interfaces.UUIDGenerator,
    ):
        self._saver = saver
        self._category_reader = category_reader
        self._uuid_generator = uuid_generator

    async def __call__(self, store_id: UUID, category_id: UUID) -> Collection[CategorySelection]:
        store_category = StoreCategory(
            id=self._uuid_generator(),
            store_id=store_id,
            category_id=category_id,
        )
        await self._saver.save(store_category=store_category)
        return await self._category_reader.get_store_category_selection(store_id=store_id)


class DeleteStoreCategoryManager(interfaces.StoreCategoryReader, interfaces.StoreCategoryDeleter, Protocol): ...


class DeleteStoreCategoryInteractor:
    def __init__(
        self,
        deleter: DeleteStoreCategoryManager,
        category_reader: interfaces.CategoryReader,
    ):
        self._deleter = deleter
        self._category_reader = category_reader

    async def __call__(self, store_id: UUID, category_id: UUID) -> Collection[CategorySelection]:
        store_category = await self._deleter.get_by_store_category_ids(store_id=store_id, category_id=category_id)
        await self._deleter.delete(store_category=store_category)
        return await self._category_reader.get_store_category_selection(store_id=store_id)
