from typing import Any, Mapping, Optional
from microapi.core.headers import HeadersView
from microapi.request.query import QueryParamsView


class Request:
    def __init__(self, scope: Mapping[str, Any], receive: Optional[Callable] = None):
        self._scope = scope
        self._receive = receive

        self._body: Optional[bytes] = None
        self._body_consumed = False

        self.method: str = scope["method"]
        self.path: str = scope["path"]
        self.raw_path: bytes = scope.get("raw_path", b"")
        self.query_string: bytes = scope.get("query_string", b"")

        self.headers = HeadersView(scope.get("headers", []))

        self._query_params: Optional[QueryParamsView] = None

    @property
    def query(self) -> QueryParamsView:
        if self._query_params is None:
            self._query_params = QueryParamsView(self.query_string)
        return self._query_params

    async def body(self) -> bytes:
        if self._body_consumed:
            return self._body or b""

            if self._receive is None:
                return b""

            chunks: list[bytes] = []
            while True:
                message = await self._receive()
                if message["type"] != "http.request":
                    break

                chunks.append(message.get("body", b""))
                if not message.get("more_body", False):
                    break

            self._body = b"".join(chunks)
            self._body_consumed = True
            return self._body
