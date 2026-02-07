class Router:
    def __init__(self):
        self.routes = {}

    def add(self, method: str, path: str, handler):
        key = (method.upper(), path)
        self.routes[key] = handler

    def match(self, method: str, path: str):
        key = (method.upper(), path)
        print('MATCH CALLED -> ', key)
        print(self.routes)
        print(self.routes.get(key))
        return self.routes.get(key)
