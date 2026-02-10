import pytest

from microapi.app import MicroAPI
from microapi.response import TextResponse
from microapi.router.trie import TrieRouter


class SendCollector:
    def __init__(self):
        self.messages = []

    async def __call__(self, message):
        self.messages.append(message)


def make_scope(method: str = "GET", path: str = "/"):
    return {
        "type": "http",
        "method": method,
        "path": path,
        "raw_path": path.encode(),
        "query_string": b"",
        "headers": [],
    }


@pytest.mark.asyncio
async def test_middleware_runs_around_handler():
    calls = []

    async def middleware(request, call_next):
        calls.append("before")
        response = await call_next(request)
        calls.append("after")
        return response

    async def handler(request):
        calls.append("handler")
        return "ok"

    router = TrieRouter()
    router.add("GET", "/", handler)

    app = MicroAPI(router)
    app.add_middleware(middleware)

    send = SendCollector()
    scope = make_scope()

    await app(scope, receive=None, send=send)

    assert calls == ["before", "handler", "after"]


@pytest.mark.asyncio
async def test_middleware_order_is_preserved():
    order = []

    async def m1(request, call_next):
        order.append("m1")
        return await call_next(request)

    async def m2(request, call_next):
        order.append("m2")
        return await call_next(request)

    async def handler(request):
        return "ok"

    router = TrieRouter()
    router.add("GET", "/", handler)

    app = MicroAPI(router)
    app.add_middleware(m1)
    app.add_middleware(m2)

    send = SendCollector()
    scope = make_scope()

    await app(scope, receive=None, send=send)

    assert order == ["m1", "m2"]


@pytest.mark.asyncio
async def test_middleware_can_short_circuit():
    async def middleware(request, call_next):
        return TextResponse("blocked", status_code=403)

    async def handler(request):
        return "ok"

    router = TrieRouter()
    router.add("GET", "/", handler)

    app = MicroAPI(router)
    app.add_middleware(middleware)

    send = SendCollector()
    scope = make_scope()

    await app(scope, receive=None, send=send)

    assert send.messages[0]["status"] == 403
