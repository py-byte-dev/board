from collections.abc import Collection
from itertools import chain
from uuid import UUID

from psycopg import AsyncConnection
from psycopg.rows import class_row

from backend.application import interfaces
from backend.domain import exceptions as domain_exceptions
from backend.domain.entities.store_resource import StoreResource


class StoreRecourceRepository(
    interfaces.StoreResourceReader,
    interfaces.StoreRecourceSaver,
    interfaces.StoreRecourceDeleter,
):
    def __init__(
        self,
        conn: AsyncConnection,
    ):
        self._conn = conn

    async def get_by_id(self, recource_id: UUID) -> StoreResource:
        async with self._conn.cursor(row_factory=class_row(StoreResource)) as cursor:
            query = 'SELECT id, title, target_url, store_id FROM store_resources WHERE id = %s'
            await cursor.execute(query, (recource_id,))
            result = await cursor.fetchone()
            if not result:
                raise domain_exceptions.StoreResourceNotFoundById
            return result

    async def get_all_by_store_id(self, store_id: UUID) -> Collection[StoreResource]:
        async with self._conn.cursor(row_factory=class_row(StoreResource)) as cursor:
            query = 'SELECT id, title, target_url, store_id FROM store_resources WHERE store_id = %s'
            await cursor.execute(query, (store_id,))
            result = await cursor.fetchall()
            return result

    async def save(self, store_resources: Collection[StoreResource]) -> None:
        values_sql = ', '.join(['(%s, %s, %s, %s)'] * len(store_resources))

        query = f'INSERT INTO store_resources (id, title, target_url, store_id) VALUES {values_sql}'

        params = list(chain.from_iterable((r.id, r.title, r.target_url, r.store_id) for r in store_resources))

        async with self._conn.cursor() as cursor:
            await cursor.execute(query, params)

    async def delete(self, store_resource: StoreResource) -> None:
        async with self._conn.cursor() as cursor:
            stmt = 'DELETE FROM store_resources WHERE id = %s'
            await cursor.execute(stmt, (store_resource.id,))
            await self._conn.commit()
