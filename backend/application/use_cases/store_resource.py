from collections.abc import Collection
from typing import Protocol
from uuid import UUID

from backend.application import interfaces
from backend.domain.entities.store_resource import StoreResource


class GetStoreResourcesInteractor:
    def __init__(
        self,
        reader: interfaces.StoreResourceReader,
    ):
        self._reader = reader

    async def __call__(self, store_id: UUID) -> Collection[StoreResource]:
        return await self._reader.get_all_by_store_id(store_id=store_id)


class AddStoreResourceManager(interfaces.StoreResourceReader, interfaces.StoreRecourceSaver, Protocol): ...


class AddStoreResourcesInteractor:
    def __init__(
        self,
        saver: AddStoreResourceManager,
        uuid_generator: interfaces.UUIDGenerator,
    ):
        self._saver = saver
        self._uuid_generator = uuid_generator

    async def __call__(self, resources_url: str, store_id: UUID) -> Collection[StoreResource]:
        store_resources = [
            StoreResource(
                id=self._uuid_generator(),
                target_url=parts[0].strip(),
                title=parts[1].strip(),
                store_id=store_id,
            )
            for parts in (line.split('|') for line in resources_url.strip().split('\n'))
        ]

        await self._saver.save(store_resources=store_resources)
        return await self._saver.get_all_by_store_id(store_id=store_id)


class DeleteStoreResourcesManager(interfaces.StoreResourceReader, interfaces.StoreRecourceDeleter, Protocol): ...


class DeleteStoreResourceInteractor:
    def __init__(
        self,
        deleter: DeleteStoreResourcesManager,
    ):
        self._deleter = deleter

    async def __call__(self, resource_id: UUID) -> Collection[StoreResource]:
        store_resource = await self._deleter.get_by_id(recource_id=resource_id)
        await self._deleter.delete(store_resource=store_resource)

        return await self._deleter.get_all_by_store_id(store_id=store_resource.store_id)
