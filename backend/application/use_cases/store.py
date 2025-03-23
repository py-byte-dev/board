import asyncio
from collections.abc import Iterable
from typing import Protocol
from uuid import UUID

from backend.application import interfaces
from backend.application.services.pagination import PaginationService
from backend.config import Config
from backend.domain.entities.media import Media, StoreMediaName
from backend.domain.entities.pagination import Pagination
from backend.domain.entities.store import Store, StoreDetails
from backend.domain.entities.store_category import StoreCategory
from backend.domain.entities.store_city import StoreCity
from backend.domain.entities.store_resource import StoreResource


class GetStoreInteractor:
    def __init__(
        self,
        reader: interfaces.StoreReader,
    ):
        self._reader = reader

    async def __call__(self, store_id: UUID) -> Store:
        return await self._reader.get_by_id(store_id=store_id)


class GetStoreDetailsInteractor:
    def __init__(
        self,
        reader: interfaces.StoreReader,
    ):
        self._reader = reader

    async def __call__(self, store_id: UUID) -> StoreDetails:
        return await self._reader.get_with_relations(store_id=store_id)


class GetAllStoresInteractor:
    def __init__(
        self,
        reader: interfaces.StoreReader,
        pagination: PaginationService,
    ):
        self._reader = reader
        self._pagination = pagination

    async def __call__(self, page: int, page_size: int) -> Pagination[Store]:
        stores = await self._reader.get_all()
        return self._pagination.create_page(page=page, page_size=page_size, items=stores)


class GetStoresByFilterInteractor:
    def __init__(
        self,
        reader: interfaces.StoreReader,
        pagination: PaginationService,
    ):
        self._reader = reader
        self._pagination = pagination

    async def __call__(
        self,
        page: int,
        page_size: int,
        store_title: str | None,
        city_title: str | None,
        categories_title: str | None,
    ) -> Pagination[Store]:
        categories_title = categories_title.split(',') if categories_title else None
        stores = await self._reader.get_by_filter(
            store_title=store_title,
            city_title=city_title,
            categories_title=categories_title,
        )

        return self._pagination.create_page(page=page, page_size=page_size, items=stores)


class CanAddStoreInteractor:
    def __init__(
        self,
        city_reader: interfaces.CityReader,
        category_reader: interfaces.CategoryReader,
    ):
        self._city_reader = city_reader
        self._category_reader = category_reader

    async def __call__(self) -> None:
        await self._city_reader.get_all()
        await self._category_reader.get_all()


class SaveStoreInteractor:
    def __init__(
        self,
        store_saver: interfaces.StoreSaver,
        store_city_saver: interfaces.StoreCitySaver,
        store_category_saver: interfaces.StoreCategorySaver,
        recources_saver: interfaces.StoreRecourceSaver,
        uuid_generator: interfaces.UUIDGenerator,
        config: Config,
        conn: interfaces.AsyncConnection,
    ):
        self._store_saver = store_saver
        self._store_city_saver = store_city_saver
        self._store_category_saver = store_category_saver
        self.recources_saver = recources_saver
        self._uuid_generator = uuid_generator
        self._config = config
        self.conn = conn

    async def __call__(
        self,
        title: str,
        description: str,
        cities: Iterable[UUID],
        categories: Iterable[UUID],
        main_page_url: str,
        resources_url: str,
        preview_media_pc: Media,
        preview_media_mobile: Media,
        main_media_pc: Media,
        main_media_mobile: Media,
        display_priority: int,
    ) -> None:
        store_id = self._uuid_generator()
        store = Store(
            id=store_id,
            title=title,
            description=description,
            preview_media_type=preview_media_pc.extension,
            main_media_type=main_media_pc.extension,
            main_page_url=main_page_url,
            display_priority=display_priority,
        )
        async with self.conn.transaction():
            await self._store_saver.save(
                store=store,
                preview_media_pc=preview_media_pc,
                preview_media_mobile=preview_media_mobile,
                main_media_pc=main_media_pc,
                main_media_mobile=main_media_mobile,
                bucket=self._config.minio.bucket,
            )

            store_cities = [
                (StoreCity(id=self._uuid_generator(), store_id=store_id, city_id=city_id)) for city_id in cities
            ]
            store_categories = [
                (StoreCategory(id=self._uuid_generator(), store_id=store_id, category_id=category_id))
                for category_id in categories
            ]
            store_resources = [
                StoreResource(
                    id=self._uuid_generator(),
                    target_url=parts[0].strip(),
                    title=parts[1].strip(),
                    store_id=store_id,
                )
                for parts in (line.split('|') for line in resources_url.strip().split('\n'))
            ]

            tasks = [
                self._store_city_saver.save_many(store_cities=store_cities),
                self._store_category_saver.save_many(store_categories=store_categories),
                self.recources_saver.save(store_resources=store_resources),
            ]
            await asyncio.gather(*tasks)


class UpdateStoreManager(interfaces.StoreReader, interfaces.StoreUpdater, Protocol): ...


class UpdateStoreTitleInteractor:
    def __init__(
        self,
        updater: UpdateStoreManager,
    ):
        self._updater = updater

    async def __call__(self, store_id: UUID, title: str) -> StoreDetails:
        store = await self._updater.get_by_id(store_id=store_id)
        store.title = title
        await self._updater.update(store=store)

        return await self._updater.get_with_relations(store_id=store_id)


class UpdateStoreDescriptionInteractor:
    def __init__(
        self,
        updater: UpdateStoreManager,
    ):
        self._updater = updater

    async def __call__(self, store_id: UUID, description: str) -> StoreDetails:
        store = await self._updater.get_by_id(store_id=store_id)
        store.description = description
        await self._updater.update(store=store)

        return await self._updater.get_with_relations(store_id=store_id)


class UpdateStorePrevieMediaPcInteractor:
    def __init__(
        self,
        updater: UpdateStoreManager,
        config: Config,
    ):
        self._updater = updater
        self._config = config

    async def __call__(self, store_id: UUID, media: Media) -> StoreDetails:
        store = await self._updater.get_by_id(store_id=store_id)
        store.preview_media_type = media.extension
        await self._updater.update_media(
            store=store,
            media=media,
            media_name=StoreMediaName.PC_PREVIEW,
            bucket=self._config.minio.bucket,
        )

        return await self._updater.get_with_relations(store_id=store_id)


class UpdateStorePrevieMediaMobileInteractor:
    def __init__(
        self,
        updater: UpdateStoreManager,
        config: Config,
    ):
        self._updater = updater
        self._config = config

    async def __call__(self, store_id: UUID, media: Media) -> StoreDetails:
        store = await self._updater.get_by_id(store_id=store_id)
        store.preview_media_type = media.extension
        await self._updater.update_media(
            store=store,
            media=media,
            media_name=StoreMediaName.MOBILE_PREVIEW,
            bucket=self._config.minio.bucket,
        )

        return await self._updater.get_with_relations(store_id=store_id)


class UpdateStoreMainMediaPcInteractor:
    def __init__(
        self,
        updater: UpdateStoreManager,
        config: Config,
    ):
        self._updater = updater
        self._config = config

    async def __call__(self, store_id: UUID, media: Media) -> StoreDetails:
        store = await self._updater.get_by_id(store_id=store_id)
        store.preview_media_type = media.extension
        await self._updater.update_media(
            store=store,
            media=media,
            media_name=StoreMediaName.PC_MAIN,
            bucket=self._config.minio.bucket,
        )

        return await self._updater.get_with_relations(store_id=store_id)


class UpdateStoreMainMediaMobileInteractor:
    def __init__(
        self,
        updater: UpdateStoreManager,
        config: Config,
    ):
        self._updater = updater
        self._config = config

    async def __call__(self, store_id: UUID, media: Media) -> StoreDetails:
        store = await self._updater.get_by_id(store_id=store_id)
        store.preview_media_type = media.extension
        await self._updater.update_media(
            store=store,
            media=media,
            media_name=StoreMediaName.MOBILE_MAIN,
            bucket=self._config.minio.bucket,
        )

        return await self._updater.get_with_relations(store_id=store_id)


class UpdateStoreMainPageUrlInteractor:
    def __init__(
        self,
        updater: UpdateStoreManager,
    ):
        self._updater = updater

    async def __call__(self, store_id: UUID, main_page_url: str) -> StoreDetails:
        store = await self._updater.get_by_id(store_id=store_id)
        store.main_page_url = main_page_url
        await self._updater.update(store=store)

        return await self._updater.get_with_relations(store_id=store_id)


class UpdateStoreDisplayPriorityInteractor:
    def __init__(
        self,
        updater: UpdateStoreManager,
    ):
        self._updater = updater

    async def __call__(self, store_id: UUID, display_priority: int) -> StoreDetails:
        store = await self._updater.get_by_id(store_id=store_id)
        store.display_priority = display_priority
        await self._updater.update(store=store)

        return await self._updater.get_with_relations(store_id=store_id)


class DeleteStoreManager(interfaces.StoreReader, interfaces.StoreDeleter, Protocol): ...


class DeleteStoreInteractor:
    def __init__(
        self,
        deleter: DeleteStoreManager,
        pagination: PaginationService,
    ):
        self._deleter = deleter
        self._pagination = pagination

    async def __call__(self, store_id: UUID, page: int, page_size: int) -> Pagination[Store]:
        store = await self._deleter.get_by_id(store_id=store_id)
        await self._deleter.delete(store=store)
        stores = await self._deleter.get_all()

        return self._pagination.create_page(page=page, page_size=page_size, items=stores)
