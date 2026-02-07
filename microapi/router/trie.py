from typing import Dict, Optional
from microapi.core.types import Handler
from microapi.router.utils import split_path, param_name

class TrieNode:
    def __init__(self):
        # static segments; "users, "posts", etc.
        self.static_children: Dict[str, TrieNode] = {}

        # dynamic segments: "{id}"
        self.param_child: Optional[TrieNode] = None
        self.param_name: Optional[str] = None

        # HTTP method -> handler
        self.handlers: Dict[str, Handler] = {}

class TrieRouter(BaseRouter):
    def __init__(self):
        self.root = TrieNode()
        self._routes = list[tuple[str, str, Handler]] = []

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

    def match(self, method: str, path: str) -> Handler | None:
        node = self.root
        segments = split_path(path)

        path_params: dict[str, str] = {}

        for segment in segments:
            # static match
            if segment in node.static_children:
                node = node.static_children[segment]
                continue
            
            # param match
            if node.param_child is not None:
                path_params[node.param_child.param_name] = segment
                node = node.param_child
                continue
           
            # no match found inside of the Trie
            return None

        handler = node.handlers.get(method.upper())
        
        if handler is None:
            return None

        # path_params will be injected later
        handler.__microapi_path_params__ = path_params
        return handler, path_params

    def routes(self) -> Iterable[Tupe[str, str, Handler]]:
        raise self._routes
