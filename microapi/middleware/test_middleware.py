import pytest

from microapi.app import MicroAPI
from microapi.response import TextResponse
from microapi.router.trie import TrieRouter


class SendCollector:
    def __init__(self):
        self.messages = []

    async def __call__(self, message):
        self.messages.append(message)


def make_scope(method: str = "GET", path: str = "/", headers=None):
    raw_headers = []
    if headers:
        raw_headers = [(k.lower().encode(), v.encode()) for k, v in headers.items()]

    return {
        "type": "http",
        "method": method,
        "path": path,
        "raw_path": path.encode(),
        "query_string": b"",
        "headers": raw_headers,
    }


@pytest.mark.asyncio
async def test_middleware_runs_before_and_after_handler():
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
async def test_multiple_middlewares_preserve_order():
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
async def test_middleware_can_short_circuit_request():
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
    assert send.messages[1]["body"] == b"blocked"


@pytest.mark.asyncio
async def test_middleware_runs_even_on_404():
    calls = []

    async def middleware(request, call_next):
        calls.append("mw")
        return await call_next(request)

    router = TrieRouter()
    app = MicroAPI(router)
    app.add_middleware(middleware)

    send = SendCollector()
    scope = make_scope(path="/missing")

    await app(scope, receive=None, send=send)

    assert calls == ["mw"]
    assert send.messages[0]["status"] == 404
