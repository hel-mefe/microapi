from microapi.core.router import BaseRouter


class SimpleRouter(BaseRouter):
    def __init__(self):
        self._routes: dict[tuple[str, str], callable] = {}

    def add(self, method: str, path: str, handler):
        self._routes[(method.upper(), path)] = handler

    def match(self, method: str, path: str):
        handler = self._routes.get((method.upper(), path))
        if handler is None:
            return None
        return handler, {}

    def allowed_methods(self, path: str) -> set[str]:
        return {method for (method, p) in self._routes.keys() if p == path}

    def routes(self):
        return self._routes
