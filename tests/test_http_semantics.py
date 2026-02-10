import pytest

from microapi.app import MicroAPI
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
async def test_404_when_path_does_not_exist():
    router = TrieRouter()
    app = MicroAPI(router)

    send = SendCollector()
    scope = make_scope("GET", "/unknown")

    await app(scope, receive=None, send=send)

    assert send.messages[0]["status"] == 404


@pytest.mark.asyncio
async def test_405_when_method_not_allowed():
    router = TrieRouter()

    async def handler(request):
        return "ok"

    router.add("GET", "/users", handler)
    app = MicroAPI(router)

    send = SendCollector()
    scope = make_scope("POST", "/users")

    await app(scope, receive=None, send=send)

    assert send.messages[0]["status"] == 405


@pytest.mark.asyncio
async def test_allow_header_on_405():
    router = TrieRouter()

    async def handler(request):
        return "ok"

    router.add("GET", "/users", handler)
    router.add("PUT", "/users", handler)

    app = MicroAPI(router)

    send = SendCollector()
    scope = make_scope("POST", "/users")

    await app(scope, receive=None, send=send)

    headers = dict(send.messages[0]["headers"])
    assert b"allow" in headers
    assert headers[b"allow"] == b"GET, PUT"
