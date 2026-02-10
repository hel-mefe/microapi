import pytest

from microapi.app import MicroAPI
from microapi.router.group import Router
from microapi.router.trie import TrieRouter


class SendCollector:
    def __init__(self):
        self.messages = []

    async def __call__(self, message):
        self.messages.append(message)


def make_scope(path="/"):
    return {
        "type": "http",
        "method": "GET",
        "path": path,
        "raw_path": path.encode(),
        "query_string": b"",
        "headers": [],
    }


@pytest.mark.asyncio
async def test_router_group_prefix():
    app = MicroAPI(router=TrieRouter())

    api = Router(prefix="/api")

    @api.get("/users")
    async def users():
        return "users"

    app.include_router(api)

    send = SendCollector()
    await app(make_scope("/api/users"), None, send)

    assert send.messages[1]["body"] == b"users"


@pytest.mark.asyncio
async def test_multiple_routes_in_group():
    app = MicroAPI(router=TrieRouter())

    api = Router(prefix="/v1")

    @api.get("/a")
    async def a():
        return "a"

    @api.get("/b")
    async def b():
        return "b"

    app.include_router(api)

    send = SendCollector()
    await app(make_scope("/v1/b"), None, send)

    assert send.messages[1]["body"] == b"b"
