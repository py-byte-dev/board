from collections.abc import Collection
from typing import Protocol
from uuid import UUID

from backend.application import interfaces
from backend.config import Config
from backend.domain.entities.banner import Banner
from backend.domain.entities.media import BannerMediaName, Media


class GetBannerInteractor:
    def __init__(
            self,
            reader: interfaces.BannerReader,
    ):
        self._reader = reader

    async def __call__(self, banner_id: UUID) -> Banner:
        return await self._reader.get_by_id(banner_id=banner_id)


class GetBannersInteractor:
    def __init__(
            self,
            reader: interfaces.BannerReader,
    ):
        self._reader = reader

    async def __call__(self) -> Collection[Banner]:
        return await self._reader.get_all()


class SaveBannerInteractor:
    def __init__(
            self,
            saver: interfaces.BannerSaver,
            uuid_generator: interfaces.UUIDGenerator,
            config: Config,
    ):
        self._saver = saver
        self._uuid_generator = uuid_generator
        self._config = config

    async def __call__(self, target_url: str, pc_media: Media, mobile_media: Media, display_priority: int) -> None:
        banner = Banner(
            id=self._uuid_generator(),
            target_url=target_url,
            media_type=pc_media.extension,
            display_priority=display_priority
        )

        await self._saver.save(
            banner=banner,
            pc_media=pc_media,
            mobile_media=mobile_media,
            bucket=self._config.minio.bucket,
        )


class UpdateBannerManager(interfaces.BannerReader, interfaces.BannerUpdater, Protocol): ...


class UpdateBannerUrlInteractor:
    def __init__(
            self,
            updater: UpdateBannerManager,
    ):
        self._updater = updater

    async def __call__(self, banner_id: UUID, target_url: str) -> Banner:
        banner = await self._updater.get_by_id(banner_id=banner_id)
        banner.target_url = target_url
        await self._updater.update(banner=banner)

        return banner


class UpdateBannerDisplayPriorityInteractor:
    def __init__(
            self,
            updater: UpdateBannerManager,
    ):
        self._updater = updater

    async def __call__(self, banner_id: UUID, display_priority: int) -> Banner:
        banner = await self._updater.get_by_id(banner_id=banner_id)
        banner.display_priority = display_priority
        await self._updater.update(banner=banner)

        return banner


class UpdatePcBannerInteractor:
    def __init__(
            self,
            updater: UpdateBannerManager,
            config: Config,
    ):
        self._updater = updater
        self._config = config

    async def __call__(self, banner_id: UUID, media: Media) -> Banner:
        banner = await self._updater.get_by_id(banner_id=banner_id)
        banner.media_type = media.extension
        await self._updater.update_media(
            banner=banner,
            media=media,
            media_name=BannerMediaName.PC,
            bucket=self._config.minio.bucket,
        )
        return banner


class UpdateMobileBannerInteractor:
    def __init__(
            self,
            updater: UpdateBannerManager,
            config: Config,
    ):
        self._updater = updater
        self._config = config

    async def __call__(self, banner_id: UUID, media: Media) -> Banner:
        banner = await self._updater.get_by_id(banner_id=banner_id)
        banner.media_type = media.extension
        await self._updater.update_media(
            banner=banner,
            media=media,
            media_name=BannerMediaName.MOBILE,
            bucket=self._config.minio.bucket,
        )
        return banner


class DeleteBannerManager(interfaces.BannerReader, interfaces.BannerDeleter, Protocol): ...


class DeleteBannerInteractor:
    def __init__(
            self,
            deleter: DeleteBannerManager,
    ):
        self._deleter = deleter

    async def __call__(self, banner_id: UUID) -> Collection[Banner]:
        banner = await self._deleter.get_by_id(banner_id=banner_id)
        await self._deleter.delete(banner=banner)
        return await self._deleter.get_all()
