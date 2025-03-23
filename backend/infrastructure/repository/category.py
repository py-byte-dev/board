from collections.abc import Collection
from itertools import chain
from uuid import UUID

from psycopg import AsyncConnection
from psycopg.rows import class_row

from backend.application import interfaces
from backend.domain import exceptions as domain_exceptions
from backend.domain.entities.category import Category, CategorySelection


class CategoryRepository(
    interfaces.CategoryReader,
    interfaces.CategorySaver,
    interfaces.CategoryUpdater,
    interfaces.CategoryDeleter,
):
    def __init__(
        self,
        conn: AsyncConnection,
    ):
        self._conn = conn

    async def get_by_id(self, category_id: UUID) -> Category:
        async with self._conn.cursor(row_factory=class_row(Category)) as cursor:
            query = 'SELECT id, title FROM categories WHERE id = %s'
            await cursor.execute(query, (category_id,))
            result = await cursor.fetchone()
            if not result:
                raise domain_exceptions.CategoryNotFoundByIdError
            return result

    async def get_all(self) -> Collection[Category]:
        async with self._conn.cursor(row_factory=class_row(Category)) as cursor:
            query = 'SELECT id, title FROM categories'
            await cursor.execute(query)
            result = await cursor.fetchall()
            if not result:
                raise domain_exceptions.CategoriesNotFoundError
            return result

    async def get_store_category_selection(self, store_id: UUID) -> Collection[CategorySelection]:
        async with self._conn.cursor(row_factory=class_row(CategorySelection)) as cursor:
            query = (
                'SELECT c.id, c.title, '
                'CASE WHEN sc.store_id IS NOT NULL THEN true ELSE false END AS is_linked '
                'FROM categories c '
                'LEFT JOIN stores_categories sc ON c.id = sc.category_id AND sc.store_id = %s'
            )
            await cursor.execute(query, (store_id,))
            results = await cursor.fetchall()
            return results

    async def save(self, categories: Collection[Category]) -> None:
        values_sql = ', '.join(['(%s, %s)'] * len(categories))

        query = f'INSERT INTO categories (id, title) VALUES {values_sql}'

        params = list(chain.from_iterable((category.id, category.title) for category in categories))

        async with self._conn.cursor() as cursor:
            await cursor.execute(query, params)
            await self._conn.commit()

    async def update(self, category: Category) -> None:
        async with self._conn.cursor() as cursor:
            stmt = 'UPDATE categories SET title = %s WHERE id = %s'
            await cursor.execute(stmt, (category.title, category.id))
            await self._conn.commit()

    async def delete(self, category: Category) -> None:
        async with self._conn.cursor() as cursor:
            stmt = 'DELETE FROM categories WHERE id = %s'
            await cursor.execute(stmt, (category.id,))
            await self._conn.commit()
