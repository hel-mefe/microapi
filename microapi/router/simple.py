from collections.abc import Iterable

from microapi.core.router import BaseRouter
from microapi.core.types import Handler


class SimpleRouter(BaseRouter):
    def __init__(self):
        self._routes = {}

    def add(self, method: str, path: str, handler):
        key = (method.upper(), path)
        self._routes[key] = handler

    def match(self, method: str, path: str):
        key = (method.upper(), path)
        return self._routes.get(key)

    def routes(self) -> Iterable[tuple[str, str, Handler]]:
        for (method, path), handler in self._routes.items():
            yield method, path, handler
