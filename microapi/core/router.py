from abc import ABC, abstractmethod

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
    def add(
        self, method: str, path: str, handler: Handler
    ) -> tuple[Handler, dict[str, str]] | None:
        """
        Register a route.
        Return (handler, path_params) or None.
        """
        raise NotImplementedError

    @abstractmethod
    def match(self, method: str, path: str) -> Handler | None:
        """
        Resolve a request to a handler.
        """
        raise NotImplementedError

    def route(self, path: str, method: str):
        def decorator(func):
            self.add(method, path, func)
            return func

        return decorator

    def get(self, path: str):
        return self.route(path, "GET")

    def post(self, path: str):
        return self.route(path, "POST")

    def put(self, path: str):
        return self.route(path, "PUT")

    def delete(self, path: str):
        return self.route(path, "DELETE")

    def patch(self, path: str):
        return self.route(path, "PATCH")
