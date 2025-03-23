import asyncio
from collections.abc import Collection
from uuid import UUID

import redis.asyncio as redis

from backend.application import interfaces
from backend.domain import exceptions as domain_exceptions
from backend.domain.entities.banner import Banner
from backend.domain.entities.media import BannerMediaName, Media
from backend.infrastructure.mapper.banner import BannerMapper


class BannerRepository(
    interfaces.BannerReader,
    interfaces.BannerSaver,
    interfaces.BannerUpdater,
    interfaces.BannerDeleter,
):
    def __init__(
        self,
        client: redis.Redis,
        mapper: BannerMapper,
        s3_client: interfaces.S3Client,
    ):
        self._client = client
        self._mapper = mapper
        self._s3_client = s3_client
        self._ids_key = 'banner:ids'

    async def get_by_id(self, banner_id: UUID) -> Banner:
        redis_key = self._banner_key(banner_id)
        data = await self._client.get(redis_key)
        if data is None:
            raise domain_exceptions.BannerNotFoundByIdError
        return self._mapper.json_to_entity(data)

    async def get_all(self) -> Collection[Banner]:
        id_strs = await self._client.smembers(self._ids_key)
        if not id_strs:
            raise domain_exceptions.BannersNotFoundError

        keys = [self._banner_key(UUID(id_str.decode())) for id_str in id_strs]
        data_list = await self._client.mget(*keys)

        banners = [self._mapper.json_to_entity(data) for data in data_list if data is not None]
        return banners

    async def save(self, banner: Banner, pc_media: Media, mobile_media: Media, bucket: str) -> None:
        redis_key = self._banner_key(banner.id)
        json_data = self._mapper.entity_to_json(banner)
        await self._client.set(redis_key, json_data)
        await self._client.sadd(self._ids_key, str(banner.id))

        media_items = [
            (BannerMediaName.PC, pc_media),
            (BannerMediaName.MOBILE, mobile_media),
        ]

        tasks = [
            self._s3_client.save(
                bucket=bucket,
                file_name=f'{banner.id}-{media_name}.{media.extension}',
                data=media.media_obj,
            )
            for media_name, media in media_items
        ]

        await asyncio.gather(*tasks)

    async def update(self, banner: Banner) -> None:
        redis_key = self._banner_key(banner.id)
        json_data = self._mapper.entity_to_json(banner)
        await self._client.set(redis_key, json_data)
        await self._client.sadd(self._ids_key, str(banner.id))

    async def update_media(self, banner: Banner, media: Media, media_name: BannerMediaName, bucket: str) -> None:
        redis_key = self._banner_key(banner.id)
        json_data = self._mapper.entity_to_json(banner)
        await self._client.set(redis_key, json_data)
        await self._client.sadd(self._ids_key, str(banner.id))

        await self._s3_client.save(
            bucket=bucket,
            file_name=f'{banner.id}-{media_name}.{media.extension}',
            data=media.media_obj,
        )

    async def delete(self, banner: Banner) -> None:
        redis_key = self._banner_key(banner.id)
        await self._client.delete(redis_key)
        await self._client.srem(self._ids_key, str(banner.id))

    @staticmethod
    def _banner_key(banner_id: UUID) -> str:
        return f'banner:{banner_id}'
