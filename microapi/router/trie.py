from microapi.core.router import BaseRouter
from microapi.router.utils import is_param, param_name, split_path


class TrieNode:
    def __init__(self):
        self.static = {}
        self.param = None
        self.param_name = None
        self.handlers = {}


class TrieRouter(BaseRouter):
    def __init__(self):
        self.root = TrieNode()

    def add(self, method: str, path: str, handler):
        node = self.root
        for segment in split_path(path):
            if is_param(segment):
                if node.param is None:
                    node.param = TrieNode()
                    node.param_name = param_name(segment)
                node = node.param
            else:
                node = node.static.setdefault(segment, TrieNode())
        node.handlers[method.upper()] = handler

    def match(self, method: str, path: str):
        node = self.root
        params = {}

        for segment in split_path(path):
            if segment in node.static:
                node = node.static[segment]
            elif node.param:
                params[node.param_name] = segment
                node = node.param
            else:
                return None

        handler = node.handlers.get(method.upper())
        if handler is None:
            return None

        return handler, params

    def allowed_methods(self, path: str) -> set[str]:
        node = self.root
        for segment in split_path(path):
            if segment in node.static:
                node = node.static[segment]
            elif node.param:
                node = node.param
            else:
                return set()
        return set(node.handlers.keys())
