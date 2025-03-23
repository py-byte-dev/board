from abc import abstractmethod
from collections.abc import Collection
from typing import Protocol
from uuid import UUID

from backend.domain.entities.store_resource import StoreResource


class StoreResourceReader(Protocol):
    @abstractmethod
    async def get_by_id(self, recource_id: UUID) -> StoreResource: ...

    @abstractmethod
    async def get_all_by_store_id(self, store_id: UUID) -> Collection[StoreResource]: ...


class StoreRecourceSaver(Protocol):
    @abstractmethod
    async def save(self, store_resources: Collection[StoreResource]) -> None: ...


class StoreRecourceDeleter(Protocol):
    @abstractmethod
    async def delete(self, store_resource: StoreResource) -> None: ...
