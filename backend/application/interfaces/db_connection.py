from abc import abstractmethod
from collections.abc import AsyncIterator
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Protocol


class AsyncTransaction(AbstractAsyncContextManager):
    @abstractmethod
    async def __aenter__(self) -> 'AsyncTransaction': ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool: ...


class AsyncConnection(Protocol):
    @abstractmethod
    async def transaction(
        self,
        savepoint_name: str | None = None,
        force_rollback: bool = False,
    ) -> AsyncIterator[AsyncTransaction]: ...
