from collections.abc import Iterable

from microapi.core.router import BaseRouter
from microapi.core.types import Handler
from microapi.router.utils import is_param, param_name, split_path


class TrieNode:
    def __init__(self):
        self.static_children: dict[str, TrieNode] = {}
        self.param_child: TrieNode | None = None
        self.param_name: str | None = None
        self.handlers: dict[str, Handler] = {}


class TrieRouter(BaseRouter):
    def __init__(self):
        self.root = TrieNode()
        self._routes: list[tuple[str, str, Handler]] = []

    def add(self, method: str, path: str, handler: Handler) -> None:
        node = self.root
        segments = split_path(path)

        for segment in segments:
            if is_param(segment):
                name = param_name(segment)

                if node.param_child is None:
                    node.param_child = TrieNode()
                    node.param_child.param_name = name

                node = node.param_child
            else:
                if segment not in node.static_children:
                    node.static_children[segment] = TrieNode()
                node = node.static_children[segment]

        node.handlers[method.upper()] = handler
        self._routes.append((method.upper(), path, handler))

    def match(self, method: str, path: str):
        node = self.root
        segments = split_path(path)
        path_params: dict[str, str] = {}

        for segment in segments:
            if segment in node.static_children:
                node = node.static_children[segment]
                continue

            if node.param_child is not None:
                path_params[node.param_child.param_name] = segment
                node = node.param_child
                continue

            return None

        handler = node.handlers.get(method.upper())
        if handler is None:
            return None

        return handler, path_params

    def allowed_methods(self, path: str) -> set[str] | None:
        node = self.root
        segments = split_path(path)

        for segment in segments:
            if segment in node.static_children:
                node = node.static_children[segment]
                continue

            if node.param_child is not None:
                node = node.param_child
                continue

            return None

        return set(node.handlers.keys())

    def routes(self) -> Iterable[tuple[str, str, Handler]]:
        return self._routes
