import pytest

from microapi.app import MicroAPI
from microapi.middleware.logging import LoggingMiddleware
from microapi.router.trie import TrieRouter


class SendCollector:
    def __init__(self):
        self.messages = []

    async def __call__(self, message):
        self.messages.append(message)


def make_scope(method="GET", path="/"):
    return {
        "type": "http",
        "method": method,
        "path": path,
        "raw_path": path.encode(),
        "query_string": b"",
        "headers": [],
    }


@pytest.mark.asyncio
async def test_logging_middleware_logs_request_and_response(capsys):
    async def handler(request):
        return "ok"

    router = TrieRouter()
    router.add("GET", "/", handler)

    app = MicroAPI(router)
    app.add_middleware(LoggingMiddleware())

    send = SendCollector()
    scope = make_scope()

    await app(scope, receive=None, send=send)

    captured = capsys.readouterr().out
    assert "GET /" in captured
    assert "200" in captured


@pytest.mark.asyncio
async def test_logging_middleware_logs_404(capsys):
    router = TrieRouter()
    app = MicroAPI(router)
    app.add_middleware(LoggingMiddleware())

    send = SendCollector()
    scope = make_scope(path="/missing")

    await app(scope, receive=None, send=send)

    captured = capsys.readouterr().out
    assert "GET /missing" in captured
    assert "404" in captured
