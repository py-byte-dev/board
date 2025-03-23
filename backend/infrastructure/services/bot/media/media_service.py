from io import BytesIO

from aiogram.types import Message

from backend.domain.entities.media import Media, MediaType
from backend.infrastructure import exceptions as infra_exceptions


class MediaService:
    async def download_media(self, message: Message) -> Media:
        file_id, extension = self._get_file_metadata(message)
        file = await message.bot.get_file(file_id=file_id)
        file_path = file.file_path
        media_obj = BytesIO()
        await message.bot.download_file(file_path=file_path, destination=media_obj)
        media_obj.seek(0)

        return Media(
            media_obj=media_obj,
            extension=extension,
        )

    @staticmethod
    def _get_file_metadata(message: Message) -> str:
        if message.content_type == 'photo':
            return message.photo[-1].file_id, MediaType.PNG
        if message.content_type == 'animation':
            return message.animation.file_id, MediaType.GIF
        raise infra_exceptions.InvalidMediaContentTypeError
