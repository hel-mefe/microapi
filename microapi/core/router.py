from abc import ABC, abstractmethod
from typing import Optional
from .types import Handler


class BaseRouter(ABC):
    """
    Router contract.

    A router:
    - stores routes
    - resolves (method, path) to a handler
    - never executes handlers
    """

    @abstractmethod
    def add(self, method: str, path: str, handler: Handler) -> Optional[tuple[Handler, dict[str, str]]]:
        """
        Register a route.
        Return (handler, path_params) or None.
        """
        raise NotImplementedError

    @abstractmethod
    def match(self, method: str, path: str) -> Optional[Handler]:
        """
        Resolve a request to a handler.
        """
        raise NotImplementedError

