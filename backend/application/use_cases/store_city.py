from collections.abc import Collection
from typing import Protocol
from uuid import UUID

from backend.application import interfaces
from backend.domain.entities.city import CitySelection
from backend.domain.entities.store_city import StoreCity


class AddStoreCityManager(interfaces.StoreCityReader, interfaces.StoreCitySaver, Protocol): ...


class AddStoreCityInteractor:
    def __init__(
        self,
        saver: AddStoreCityManager,
        city_reader: interfaces.CityReader,
        uuid_generator: interfaces.UUIDGenerator,
    ):
        self._saver = saver
        self._city_reader = city_reader
        self._uuid_generator = uuid_generator

    async def __call__(self, store_id: UUID, city_id: UUID) -> Collection[CitySelection]:
        store_city = StoreCity(
            id=self._uuid_generator(),
            store_id=store_id,
            city_id=city_id,
        )
        await self._saver.save(store_city=store_city)
        return await self._city_reader.get_store_city_selection(store_id=store_id)


class DeleteStoreCityManager(interfaces.StoreCityReader, interfaces.StoreCityDeleter, Protocol): ...


class DeleteStoreCityInteractor:
    def __init__(
        self,
        city_reader: interfaces.CityReader,
        deleter: DeleteStoreCityManager,
    ):
        self._city_reader = city_reader
        self._deleter = deleter

    async def __call__(self, store_id: UUID, city_id: UUID) -> Collection[CitySelection]:
        store_city = await self._deleter.get_by_store_city_ids(store_id=store_id, city_id=city_id)
        await self._deleter.delete(store_city=store_city)
        return await self._city_reader.get_store_city_selection(store_id=store_id)
