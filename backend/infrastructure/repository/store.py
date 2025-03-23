import asyncio
from collections.abc import Collection
from uuid import UUID

from psycopg import AsyncConnection
from psycopg.rows import class_row, dict_row

from backend.application import interfaces
from backend.domain import exceptions as domain_exceptions
from backend.domain.entities.media import Media, StoreMediaName
from backend.domain.entities.store import Store, StoreDetails
from backend.infrastructure.mapper.store import StoreMapper


class StoreRepository(
    interfaces.StoreReader,
    interfaces.StoreSaver,
    interfaces.StoreUpdater,
    interfaces.StoreDeleter,
):
    def __init__(
        self,
        conn: AsyncConnection,
        mapper: StoreMapper,
        s3_client: interfaces.S3Client,
    ):
        self._conn = conn
        self._mapper = mapper
        self._s3_client = s3_client

    async def get_by_id(self, store_id: UUID) -> Store:
        async with self._conn.cursor(row_factory=class_row(Store)) as cursor:
            query = (
                'SELECT id, title, description, preview_media_type, main_media_type, main_page_url, display_priority '
                'FROM stores WHERE id = %s'
            )
            await cursor.execute(query, (store_id,))
            result = await cursor.fetchone()
            if not result:
                raise domain_exceptions.StoreNotFoundByIdError
            return result

    async def get_with_relations(self, store_id: UUID) -> StoreDetails:
        async with self._conn.cursor(row_factory=dict_row) as cursor:
            query = (
                'SELECT '
                '    s.id AS store_id, '
                '    s.title AS store_title, '
                '    s.description, '
                '    s.preview_media_type, '
                '    s.main_media_type, '
                '    s.main_page_url, '
                '    s.display_priority, '
                '    COALESCE( '
                '        json_agg( '
                "            DISTINCT jsonb_build_object('id', c.id, 'title', c.title) "
                '        ) FILTER (WHERE c.id IS NOT NULL), '
                "        '[]' "
                '    ) AS cities, '
                '    COALESCE( '
                '        json_agg( '
                "            DISTINCT jsonb_build_object('id', cat.id, 'title', cat.title) "
                '        ) FILTER (WHERE cat.id IS NOT NULL), '
                "        '[]' "
                '    ) AS categories, '
                '    COALESCE( '
                '        json_agg( '
                '            DISTINCT '
                "jsonb_build_object('id', sr.id, 'title', sr.title, 'target_url', sr.target_url, 'store_id', sr.store_id) "
                '        ) FILTER (WHERE sr.id IS NOT NULL), '
                "        '[]' "
                '    ) AS resources '
                'FROM stores AS s '
                'LEFT JOIN stores_cities AS sc ON s.id = sc.store_id '
                'LEFT JOIN cities AS c ON sc.city_id = c.id '
                'LEFT JOIN stores_categories AS sc2 ON s.id = sc2.store_id '
                'LEFT JOIN categories AS cat ON sc2.category_id = cat.id '
                'LEFT JOIN store_resources AS sr ON sr.store_id = s.id '
                'WHERE s.id = %s '
                'GROUP BY s.id;'
            )

            await cursor.execute(query, (store_id,))
            result = await cursor.fetchone()
            if not result:
                raise domain_exceptions.StoreNotFoundByIdError

            return self._mapper.result_to_store_details(result=result)

    async def get_all(self) -> Collection[Store]:
        async with self._conn.cursor(row_factory=class_row(Store)) as cursor:
            query = (
                'SELECT id, title, description, preview_media_type, main_media_type, main_page_url, display_priority '
                'FROM stores ORDER BY display_priority DESC'
            )
            await cursor.execute(query)
            result = await cursor.fetchall()
            if not result:
                raise domain_exceptions.StoresNotFoundError
            return result

    async def get_by_filter(
        self,
        store_title: str,
        city_title: str,
        categories_title: Collection[str],
    ) -> Collection[Store]:
        async with self._conn.cursor(row_factory=class_row(Store)) as cursor:
            query = (
                'SELECT DISTINCT '
                's.id, '
                's.title, '
                's.description, '
                's.preview_media_type, '
                's.main_media_type, '
                's.main_page_url, '
                's.display_priority '
                'FROM stores s '
                'JOIN stores_cities sc ON s.id = sc.store_id '
                'JOIN cities c ON sc.city_id = c.id '
                'JOIN stores_categories sc2 ON s.id = sc2.store_id '
                'JOIN categories cat ON sc2.category_id = cat.id '
                'WHERE s.title ILIKE %s '
            )

            filters = [f'%{store_title}%' if store_title else '%']

            if city_title:
                query += ' AND c.title ILIKE %s '
                filters.append(f'%{city_title}%')

            if categories_title:
                query += ' AND cat.title = ANY(%s) '
                filters.append(list(categories_title))

            query += 'ORDER BY s.display_priority;'

            await cursor.execute(query, filters)
            result = await cursor.fetchall()
            if not result:
                raise domain_exceptions.StoresNotFoundByFiltersError
            return result

    async def save(
        self,
        store: Store,
        preview_media_pc: Media,
        preview_media_mobile: Media,
        main_media_pc: Media,
        main_media_mobile: Media,
        bucket: str,
    ) -> None:
        async with self._conn.cursor() as cursor:
            stmt = (
                'INSERT INTO stores '
                '(id, title, description, preview_media_type, main_media_type, main_page_url, display_priority) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s)'
            )

            await cursor.execute(
                stmt,
                (
                    store.id,
                    store.title,
                    store.description,
                    store.preview_media_type,
                    store.main_media_type,
                    store.main_page_url,
                    store.display_priority,
                ),
            )

            media_items = [
                (StoreMediaName.PC_PREVIEW, preview_media_pc),
                (StoreMediaName.MOBILE_PREVIEW, preview_media_mobile),
                (StoreMediaName.PC_MAIN, main_media_pc),
                (StoreMediaName.MOBILE_MAIN, main_media_mobile),
            ]

            tasks = [
                self._s3_client.save(
                    bucket=bucket,
                    file_name=f'{store.id}-{media_name}.{media.extension}',
                    data=media.media_obj,
                )
                for media_name, media in media_items
            ]

            await asyncio.gather(*tasks)

    async def update(self, store: Store) -> None:
        async with self._conn.cursor() as cursor:
            stmt = (
                'UPDATE stores SET '
                'title = %s, '
                'description = %s, '
                'preview_media_type = %s, '
                'main_media_type = %s, '
                'main_page_url = %s, '
                'display_priority = %s '
                'WHERE id = %s'
            )
            await cursor.execute(
                stmt,
                (
                    store.title,
                    store.description,
                    store.preview_media_type,
                    store.main_media_type,
                    store.main_page_url,
                    store.display_priority,
                    store.id,
                ),
            )

            await self._conn.commit()

    async def update_media(self, store: Store, media: Media, media_name: StoreMediaName, bucket: str) -> None:
        async with self._conn.cursor() as cursor:
            stmt = 'UPDATE stores SET preview_media_type = %s, main_media_type = %s WHERE id = %s'
            await cursor.execute(stmt, (store.preview_media_type, store.main_media_type, store.id))

            await self._conn.commit()

            await self._s3_client.save(
                bucket=bucket,
                file_name=f'{store.id}-{media_name}.{media.extension}',
                data=media.media_obj,
            )

    async def delete(self, store: Store) -> None:
        async with self._conn.cursor() as cursor:
            stmt = 'DELETE FROM stores WHERE id = %s'
            await cursor.execute(stmt, (store.id,))
            await self._conn.commit()
