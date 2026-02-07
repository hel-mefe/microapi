class Request:
    def __init__(self, scope):
        self._scope = scope
        self.method: str = scope["method"]
        self.path: str = scope["path"]
        self.raw_path: bytes = scope.get("raw_bytes", b"")
        self.query_string: bytes = scope.get("query_string", b"")
        self.headers = self._build_headers(scope)

    def _build_headers(self, scope):
        headers = {}
        for key, value in scope.get("headers", []):
            headers[key.decode().lower()] = value.decode()

        return headers
