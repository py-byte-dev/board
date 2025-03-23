from collections.abc import Collection
from itertools import chain
from uuid import UUID

from psycopg import AsyncConnection
from psycopg.rows import class_row

from backend.application import interfaces
from backend.domain.entities.store_category import StoreCategory


class StoreCategoryRepository(
    interfaces.StoreCategoryReader,
    interfaces.StoreCategorySaver,
    interfaces.StoreCategoryDeleter,
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

    async def get_by_store_category_ids(self, store_id: UUID, category_id: UUID) -> StoreCategory:
        async with self._conn.cursor(row_factory=class_row(StoreCategory)) as cursor:
            query = 'SELECT id, store_id, category_id FROM stores_categories WHERE store_id = %s AND category_id = %s'
            await cursor.execute(query, (store_id, category_id))
            result = await cursor.fetchone()
            if not result:
                raise
            return result

    async def get_by_id(self, store_category_id: UUID) -> StoreCategory:
        async with self._conn.cursor(row_factory=class_row(StoreCategory)) as cursor:
            query = 'SELECT id, store_id, category_id FROM stores_categories WHERE store_id = %s'
            await cursor.execute(query, (store_category_id,))
            result = await cursor.fetchone()
            if not result:
                raise
            return result

    async def save(self, store_category: StoreCategory) -> None:
        async with self._conn.cursor() as cursor:
            query = 'INSERT INTO stores_categories (id, store_id, category_id) VALUES (%s, %s, %s)'
            await cursor.execute(query, (store_category.id, store_category.store_id, store_category.category_id))
            await self._conn.commit()

    async def save_many(self, store_categories: Collection[StoreCategory]) -> None:
        values_sql = ', '.join(['(%s, %s, %s)'] * len(store_categories))

        query = f'INSERT INTO stores_categories (id, store_id, category_id) VALUES {values_sql}'

        params = list(
            chain.from_iterable(
                (store_category.id, store_category.store_id, store_category.category_id)
                for store_category in store_categories
            ),
        )

        async with self._conn.cursor() as cursor:
            await cursor.execute(query, params)

    async def delete(self, store_category: StoreCategory) -> None:
        async with self._conn.cursor() as cursor:
            query = 'DELETE FROM stores_categories WHERE id = %s'
            await cursor.execute(query, (store_category.id,))
            await self._conn.commit()
