from abc import abstractmethod
from collections.abc import Collection
from typing import Protocol
from uuid import UUID

from backend.domain.entities.store_city import StoreCity


class StoreCityReader(Protocol):
    @abstractmethod
    async def relationship_exists(self, store_id: UUID, city_id: UUID) -> bool: ...

    @abstractmethod
    async def get_by_store_city_ids(self, store_id: UUID, city_id: UUID) -> StoreCity: ...

    @abstractmethod
    async def get_by_id(self, store_city_id: UUID) -> StoreCity: ...


class StoreCitySaver(Protocol):
    @abstractmethod
    async def save(self, store_city: StoreCity) -> None: ...

    @abstractmethod
    async def save_many(self, store_cities: Collection[StoreCity]) -> None: ...


class StoreCityDeleter(Protocol):
    @abstractmethod
    async def delete(self, store_city: StoreCity) -> None: ...
