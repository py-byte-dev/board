from collections.abc import Collection
from itertools import chain
from uuid import UUID

from psycopg import AsyncConnection
from psycopg.rows import class_row

from backend.application import interfaces
from backend.domain import exceptions as domain_exceptions
from backend.domain.entities.city import City, CitySelection


class CityRepository(
    interfaces.CityReader,
    interfaces.CitySaver,
    interfaces.CityDeleter,
):
    def __init__(
        self,
        conn: AsyncConnection,
    ):
        self._conn = conn

    async def get_by_id(self, city_id: UUID) -> City:
        async with self._conn.cursor(row_factory=class_row(City)) as cursor:
            query = 'SELECT id, title FROM cities WHERE id = %s'
            await cursor.execute(query, (city_id,))
            result = await cursor.fetchone()
            if not result:
                raise domain_exceptions.CityNotFoundByIdError
            return result

    async def get_all(self) -> Collection[City]:
        async with self._conn.cursor(row_factory=class_row(City)) as cursor:
            query = 'SELECT id, title FROM cities'
            await cursor.execute(query)
            results = await cursor.fetchall()
            if not results:
                raise domain_exceptions.CitiesNotFoundError
            return results

    async def get_store_city_selection(self, store_id: UUID) -> Collection[CitySelection]:
        async with self._conn.cursor(row_factory=class_row(CitySelection)) as cursor:
            query = (
                'SELECT c.id, c.title, '
                'CASE WHEN sc.store_id IS NOT NULL THEN true ELSE false END AS is_linked '
                'FROM cities c '
                'LEFT JOIN stores_cities sc ON c.id = sc.city_id AND sc.store_id = %s'
            )
            await cursor.execute(query, (store_id,))
            results = await cursor.fetchall()
            return results

    async def save(self, cities: Collection[City]) -> None:
        values_sql = ', '.join(['(%s, %s)'] * len(cities))

        query = f'INSERT INTO cities (id, title) VALUES {values_sql}'

        params = list(chain.from_iterable((city.id, city.title) for city in cities))

        async with self._conn.cursor() as cursor:
            await cursor.execute(query, params)
            await self._conn.commit()

    async def delete(self, city: City) -> None:
        async with self._conn.cursor(row_factory=class_row(City)) as cursor:
            stmt = 'DELETE FROM cities WHERE id = %s'
            await cursor.execute(stmt, (city.id,))
            await self._conn.commit()
