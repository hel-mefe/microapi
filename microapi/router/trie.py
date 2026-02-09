from typing import Dict, Optional, Tuple, Iterable

from microapi.core.router import BaseRouter
from microapi.core.types import Handler
from microapi.router.utils import split_path, is_param, param_name


class TrieNode:
    def __init__(self):
        # Static segments: "users", "posts", etc.
        self.static_children: Dict[str, "TrieNode"] = {}

        # Dynamic segment: "{id}"
        self.param_child: Optional["TrieNode"] = None
        self.param_name: Optional[str] = None

        # HTTP method -> handler
        self.handlers: Dict[str, Handler] = {}


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

    def match(
        self, method: str, path: str
    ) -> Optional[tuple[Handler, dict[str, str]]]:
        node = self.root
        segments = split_path(path)
        params: dict[str, str] = {}

        for segment in segments:
            # 1. Static match has priority
            if segment in node.static_children:
                node = node.static_children[segment]
                continue

            # 2. Dynamic match
            if node.param_child is not None:
                params[node.param_child.param_name] = segment
                node = node.param_child
                continue

            # 3. No match
            return None

        handler = node.handlers.get(method.upper())
        if handler is None:
            return None

        return handler, params

    def routes(self) -> Iterable[Tuple[str, str, Handler]]:
        return self._routes

