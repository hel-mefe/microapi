from microapi.core.router import BaseRouter

class SimpleRouter(BaseRouter):
    def __init__(self):
        self.routes = {}

    def add(self, method: str, path: str, handler):
        key = (method.upper(), path)
        self.routes[key] = handler

    def match(self, method: str, path: str):
        key = (method.upper(), path)
        return self.routes.get(key)
