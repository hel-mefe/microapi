from typing import Any, Mapping, Optional, Callable, Awaitable
import json

from microapi.core.request import Request as RequestInterface
from microapi.core.headers import HeadersView
from microapi.request.query import QueryParamsView


class State:
    """
    Per-request mutable state.
    """
    pass


class ASGIRequest(RequestInterface):
    """
    Concrete ASGI-backed request implementation.
    """

    def __init__(
        self,
        scope: Mapping[str, Any],
        receive: Optional[Callable[[], Awaitable[dict]]] = None,
    ):
        self._scope = scope
        self._receive = receive

        self.method: str = scope["method"]
        self.path: str = scope["path"]

        self.headers = HeadersView(scope.get("headers", []))
        self.path_params: dict[str, str] = {}
        self.state = State()

        self._query_string: bytes = scope.get("query_string", b"")
        self._query: Optional[QueryParamsView] = None

        self._body: Optional[bytes] = None
        self._body_consumed: bool = False


    @property
    def query(self) -> QueryParamsView:
        if self._query is None:
            self._query = QueryParamsView(self._query_string)
        return self._query

    async def body(self) -> bytes:
        if self._body_consumed:
            return self._body or b""

        if self._receive is None:
            self._body = b""
            self._body_consumed = True
            return self._body

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


    async def json(self) -> Any:
        body = await self.body()
        return json.loads(body.decode("utf-8"))

