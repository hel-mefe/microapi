from collections.abc import Callable
from typing import Any


class Registry:
    def __init__(self):
        self._providers: dict[str, Callable[[], Any]] = {}
        self._scopes: dict[str, str] = {}
        self._app_cache: dict[str, Any] = {}
        self._on_startup: dict[str, Callable[[], Any] | None] = {}
        self._on_shutdown: dict[str, Callable[[Any], Any] | None] = {}

    def register(
        self,
        name: str,
        factory: Callable[[], Any],
        *,
        scope: str = "app",
        on_startup: Callable[[], Any] | None = None,
        on_shutdown: Callable[[Any], Any] | None = None,
    ):
        if scope not in {"app", "request"}:
            raise ValueError("scope must be 'app' or 'request'")

        self._providers[name] = factory
        self._scopes[name] = scope
        self._on_startup[name] = on_startup
        self._on_shutdown[name] = on_shutdown

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

    async def startup(self):
        for name, scope in self._scopes.items():
            if scope != "app":
                continue

            if self._on_startup.get(name):
                result = self._on_startup[name]()
                if hasattr(result, "__await__"):
                    await result

            if name not in self._app_cache:
                self._app_cache[name] = self._providers[name]()

    async def shutdown(self):
        for name in reversed(list(self._app_cache.keys())):
            handler = self._on_shutdown.get(name)
            if handler:
                result = handler(self._app_cache[name])
                if hasattr(result, "__await__"):
                    await result

        self._app_cache.clear()
