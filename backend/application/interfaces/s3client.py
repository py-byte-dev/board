from abc import abstractmethod
from io import BytesIO
from pathlib import Path
from typing import Protocol


class S3Client(Protocol):
    base_path: Path

    @abstractmethod
    async def save(self, bucket: str, file_name: str, data: BytesIO) -> None: ...

    @abstractmethod
    async def get_temporary_url(self, bucket: str, file_name: str) -> str: ...
