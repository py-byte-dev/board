import mimetypes
from io import BytesIO

from miniopy_async import Minio

from backend.application import interfaces


class S3Client(interfaces.S3Client):
    def __init__(
        self,
        client: Minio,
    ):
        self._client = client

    async def save(self, bucket: str, file_name: str, data: BytesIO) -> None:
        content_type, _ = mimetypes.guess_type(file_name)
        print(content_type)

        await self._client.put_object(
            bucket_name=bucket,
            object_name=file_name,
            data=data,
            length=len(data.getbuffer()),
            content_type=content_type,
        )

    async def get_temporary_url(self, bucket: str, file_name: str) -> str:
        return await self._client.presigned_get_object(bucket_name=bucket, object_name=file_name)
