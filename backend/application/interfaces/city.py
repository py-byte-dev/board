from abc import abstractmethod
from collections.abc import Collection
from typing import Protocol
from uuid import UUID

from backend.domain.entities.city import City, CitySelection


class CityReader(Protocol):
    @abstractmethod
    async def get_by_id(self, city_id: UUID) -> City: ...

    @abstractmethod
    async def get_all(self) -> Collection[City]: ...

    @abstractmethod
    async def get_store_city_selection(self, store_id: UUID) -> Collection[CitySelection]: ...


class CitySaver(Protocol):
    @abstractmethod
    async def save(self, cities: Collection[City]) -> None: ...


class CityDeleter(Protocol):
    @abstractmethod
    async def delete(self, city: City) -> None: ...
