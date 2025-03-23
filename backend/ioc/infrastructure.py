from collections.abc import AsyncIterable

import redis.asyncio as redis
from dishka import AnyOf, Provider, Scope, provide
from miniopy_async import Minio
from psycopg import AsyncConnection
from psycopg_pool import AsyncConnectionPool

from backend.application import interfaces
from backend.application.use_cases.banner import DeleteBannerManager, UpdateBannerManager
from backend.application.use_cases.category import DeleteCategoryManager
from backend.application.use_cases.city import DeleteCityManager
from backend.application.use_cases.store import DeleteStoreManager, UpdateStoreManager
from backend.application.use_cases.store_category import AddStoreCategoryManager, DeleteStoreCategoryManager
from backend.application.use_cases.store_city import AddStoreCityManager, DeleteStoreCityManager
from backend.application.use_cases.store_resource import AddStoreResourceManager, DeleteStoreResourcesManager
from backend.config import Config
from backend.infrastructure.mapper.banner import BannerMapper
from backend.infrastructure.mapper.store import StoreMapper
from backend.infrastructure.repository.banner import BannerRepository
from backend.infrastructure.repository.category import CategoryRepository
from backend.infrastructure.repository.city import CityRepository
from backend.infrastructure.repository.store import StoreRepository
from backend.infrastructure.repository.store_category import StoreCategoryRepository
from backend.infrastructure.repository.store_city import StoreCityRepository
from backend.infrastructure.repository.store_recource import StoreRecourceRepository
from backend.infrastructure.services.bot.helpers.items_displayer import ItemsDisplayer
from backend.infrastructure.services.bot.keyboard.inline import KeyboardBuilder
from backend.infrastructure.services.bot.media.media_service import MediaService
from backend.infrastructure.services.s3.s3_client import S3Client


class InfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_connection_pool(self, config: Config) -> AsyncIterable[AsyncConnectionPool]:
        pool = AsyncConnectionPool(
            conninfo=config.pg.create_connection_string(),
            min_size=40,
            max_size=80,
            open=False,
        )
        await pool.open()
        try:
            yield pool
        finally:
            await pool.close()

    @provide(scope=Scope.REQUEST, provides=AnyOf[interfaces.AsyncConnection, AsyncConnection])
    async def get_connection(self, pool: AsyncConnectionPool) -> AsyncIterable[AsyncConnection]:
        async with pool.connection() as conn:
            yield conn

    @provide(scope=Scope.APP)
    async def get_redis_connection_pool(self, config: Config) -> AsyncIterable[redis.ConnectionPool]:
        pool = redis.ConnectionPool.from_url(url=config.redis.create_connection_string())
        yield pool
        await pool.aclose()

    @provide(scope=Scope.REQUEST)
    async def get_redis_client(self, pool: redis.ConnectionPool) -> AsyncIterable[redis.Redis]:
        client = redis.Redis(connection_pool=pool)
        yield client
        await client.aclose()

    @provide(scope=Scope.REQUEST)
    async def get_minio_client(self, config: Config) -> Minio:
        client = Minio(
            endpoint=config.minio.url,
            access_key=config.minio.user,
            secret_key=config.minio.password,
            secure=True,
        )

        return client

    city_repo = provide(
        CityRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[interfaces.CityReader, interfaces.CitySaver, DeleteCityManager],
    )

    category_repo = provide(
        CategoryRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[interfaces.CategoryReader, interfaces.CategorySaver, DeleteCategoryManager],
    )

    store_mapper = provide(
        StoreMapper,
        scope=Scope.REQUEST,
    )
    store_repo = provide(
        StoreRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[interfaces.StoreReader, interfaces.StoreSaver, UpdateStoreManager, DeleteStoreManager],
    )

    store_city_repo = provide(
        StoreCityRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[AddStoreCityManager, DeleteStoreCityManager, interfaces.StoreCitySaver],
    )

    store_category_repo = provide(
        StoreCategoryRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[AddStoreCategoryManager, DeleteStoreCategoryManager, interfaces.StoreCategorySaver],
    )

    store_recource_repo = provide(
        StoreRecourceRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[
            interfaces.StoreResourceReader,
            interfaces.StoreRecourceSaver,
            DeleteStoreResourcesManager,
            AddStoreResourceManager,
        ],
    )

    banner_mapper = provide(
        BannerMapper,
        scope=Scope.REQUEST,
    )
    banner_repo = provide(
        BannerRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[interfaces.BannerReader, interfaces.BannerSaver, DeleteBannerManager, UpdateBannerManager],
    )

    keyboard_builder = provide(
        KeyboardBuilder,
        scope=Scope.REQUEST,
        provides=interfaces.KeyboardBuilder,
    )

    media_service = provide(
        MediaService,
        scope=Scope.REQUEST,
    )

    s3_client = provide(
        S3Client,
        scope=Scope.REQUEST,
        provides=interfaces.S3Client,
    )

    items_displayer = provide(ItemsDisplayer, scope=Scope.REQUEST)
