from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any

from microapi.core.headers import HeadersView


class Request(ABC):
    """
    Request contract.

    Defines the interface exposed to handlers.
    Concrete implementations may vary.
    """

    method: str
    path: str
    headers: HeadersView
    path_params: dict[str, str]
    state: Any

    @property
    @abstractmethod
    def query(self) -> Mapping[str, list[str]]:
        raise NotImplementedError

    @abstractmethod
    async def body(self) -> bytes:
        raise NotImplementedError

    @abstractmethod
    async def json(self) -> Any:
        raise NotImplementedError
