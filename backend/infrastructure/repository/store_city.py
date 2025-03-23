from collections.abc import Collection
from itertools import chain
from uuid import UUID

from psycopg import AsyncConnection
from psycopg.rows import class_row

from backend.application import interfaces
from backend.domain.entities.store_city import StoreCity


class StoreCityRepository(
    interfaces.StoreCityReader,
    interfaces.StoreCitySaver,
    interfaces.StoreCityDeleter,
):
    def __init__(
        self,
        conn: AsyncConnection,
    ):
        self._conn = conn

    async def relationship_exists(self, store_id: UUID, city_id: UUID) -> bool:
        async with self._conn.cursor() as cursor:
            query = 'SELECT EXISTS(SELECT 1 FROM stores_cities WHERE store_id = %s AND city_id = %s)'
            await cursor.execute(query, (store_id, city_id))
            result = await cursor.fetchone()
            return result[0]

    async def get_by_store_city_ids(self, store_id: UUID, city_id: UUID) -> StoreCity:
        async with self._conn.cursor(row_factory=class_row(StoreCity)) as cursor:
            query = 'SELECT id, store_id, city_id FROM stores_cities WHERE store_id = %s AND city_id = %s'
            await cursor.execute(query, (store_id, city_id))
            result = await cursor.fetchone()
            if not result:
                raise
            return result

    async def get_by_id(self, store_city_id: UUID) -> StoreCity:
        async with self._conn.cursor(row_factory=class_row(StoreCity)) as cursor:
            query = 'SELECT id, store_id, city_id FROM stores_cities WHERE store_id = %s'
            await cursor.execute(query, (store_city_id,))
            result = await cursor.fetchone()
            if not result:
                raise
            return result

    async def save(self, store_city: StoreCity) -> None:
        async with self._conn.cursor() as cursor:
            query = 'INSERT INTO stores_cities (id, store_id, city_id) VALUES (%s, %s, %s)'
            await cursor.execute(query, (store_city.id, store_city.store_id, store_city.city_id))
            await self._conn.commit()

    async def save_many(self, store_cities: Collection[StoreCity]) -> None:
        values_sql = ', '.join(['(%s, %s, %s)'] * len(store_cities))

        query = f'INSERT INTO stores_cities (id, store_id, city_id) VALUES {values_sql}'

        params = list(
            chain.from_iterable(
                (store_city.id, store_city.store_id, store_city.city_id) for store_city in store_cities
            ),
        )

        async with self._conn.cursor() as cursor:
            await cursor.execute(query, params)

    async def delete(self, store_city: StoreCity) -> None:
        async with self._conn.cursor() as cursor:
            query = 'DELETE FROM stores_cities WHERE id = %s'
            await cursor.execute(query, (store_city.id,))
            await self._conn.commit()
