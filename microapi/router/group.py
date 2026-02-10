class Router:
    def __init__(self, prefix: str = "", middleware=None):
        self.prefix = prefix.rstrip("/")
        self.middleware = middleware or []
        self._routes: list[tuple[str, str, callable]] = []

    def add(self, method: str, path: str, handler):
        full_path = self.prefix + path
        if not full_path.startswith("/"):
            full_path = "/" + full_path
        self._routes.append((method.upper(), full_path, handler))

    def route(self, path: str, method: str):
        def decorator(func):
            self.add(method, path, func)
            return func

        return decorator

    def get(self, path: str):
        return self.route(path, "GET")

    def post(self, path: str):
        return self.route(path, "POST")

    def put(self, path: str):
        return self.route(path, "PUT")

    def delete(self, path: str):
        return self.route(path, "DELETE")

    def patch(self, path: str):
        return self.route(path, "PATCH")
