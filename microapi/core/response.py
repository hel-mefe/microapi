from abc import ABC, abstractmethod
from typing import Dict

Headers = Dict[str, str]


class Response(ABC):
    """
    Base HTTP response.
    """

    def __init__(
        self,
        status_code: int = 200,
        headers: Headers | None = None,
    ):
        self.status_code = status_code
        self.headers: Headers = headers or {}

    @abstractmethod
    async def send(self, send) -> None:
        """
        Send ASGI response messages.
        """
        raise NotImplementedError

