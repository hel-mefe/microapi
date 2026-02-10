from collections.abc import Callable
from typing import Any


class Registry:
    def __init__(self):
        self._providers: dict[str, Callable[[], Any]] = {}
        self._scopes: dict[str, str] = {}
        self._app_cache: dict[str, Any] = {}

    def register(self, name: str, factory: Callable[[], Any], scope: str = "app"):
        if scope not in {"app", "request"}:
            raise ValueError("scope must be 'app' or 'request'")
        self._providers[name] = factory
        self._scopes[name] = scope

    def resolve(self, name: str, request_cache: dict[str, Any]):
        if name not in self._providers:
            raise KeyError(f"Dependency '{name}' is not registered")

        scope = self._scopes[name]
        factory = self._providers[name]

        if scope == "app":
            if name not in self._app_cache:
                self._app_cache[name] = factory()
            return self._app_cache[name]

        if scope == "request":
            if name not in request_cache:
                request_cache[name] = factory()
            return request_cache[name]
