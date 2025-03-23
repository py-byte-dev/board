from collections.abc import Collection
from typing import Protocol
from uuid import UUID

from backend.application import interfaces
from backend.domain.entities.city import City, CitySelection


class GetCityInteractor:
    def __init__(
        self,
        reader: interfaces.CityReader,
    ):
        self._reader = reader

    async def __call__(self, city_id: UUID) -> City:
        return await self._reader.get_by_id(city_id=city_id)


class GetAllCitiesInteractor:
    def __init__(
        self,
        reader: interfaces.CityReader,
    ):
        self._reader = reader

    async def __call__(self) -> Collection[City]:
        return await self._reader.get_all()


class GetStoreCitiesInteractor:
    def __init__(
        self,
        reader: interfaces.CityReader,
    ):
        self._reader = reader

    async def __call__(self, store_id: UUID) -> Collection[CitySelection]:
        return await self._reader.get_store_city_selection(store_id=store_id)


class SaveCitiesInteractor:
    def __init__(
        self,
        saver: interfaces.CitySaver,
        uuid_generator: interfaces.UUIDGenerator,
    ):
        self._saver = saver
        self._uuid_generator = uuid_generator

    async def __call__(self, titles: str) -> None:
        cities = [City(id=self._uuid_generator(), title=title.strip()) for title in titles.split('\n')]

        await self._saver.save(cities=cities)


class DeleteCityManager(interfaces.CityReader, interfaces.CityDeleter, Protocol): ...


class DeleteCityInteractor:
    def __init__(
        self,
        deleter: DeleteCityManager,
    ):
        self._deleter = deleter

    async def __call__(self, city_id: UUID) -> Collection[City]:
        city = await self._deleter.get_by_id(city_id=city_id)
        await self._deleter.delete(city=city)

        return await self._deleter.get_all()
