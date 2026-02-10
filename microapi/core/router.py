class BaseRouter:
    def add(self, method: str, path: str, handler):
        raise NotImplementedError

    def match(self, method: str, path: str):
        raise NotImplementedError

    def allowed_methods(self, path: str) -> set[str]:
        raise NotImplementedError

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
