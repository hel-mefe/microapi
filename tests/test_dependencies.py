import pytest

from microapi.app import MicroAPI
from microapi.dependencies import Depends
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
async def test_callable_dependency():
    async def dep():
        return "value"

    async def handler(x=Depends(dep)):
        return x

    router = TrieRouter()
    router.add("GET", "/", handler)

    app = MicroAPI(router)

    send = SendCollector()
    await app(make_scope(), None, send)

    assert send.messages[1]["body"] == b"value"


@pytest.mark.asyncio
async def test_registry_app_scoped_dependency():
    async def handler(db=Depends("db")):
        return db

    router = TrieRouter()
    router.add("GET", "/", handler)

    app = MicroAPI(router)
    app.registry.register("db", lambda: "db-conn", scope="app")

    send = SendCollector()
    await app(make_scope(), None, send)

    assert send.messages[1]["body"] == b"db-conn"


@pytest.mark.asyncio
async def test_dependency_can_receive_request():
    async def dep(request):
        return request.path

    async def handler(path=Depends(dep)):
        return path

    router = TrieRouter()
    router.add("GET", "/test", handler)

    app = MicroAPI(router)

    send = SendCollector()
    await app(make_scope("/test"), None, send)

    assert send.messages[1]["body"] == b"/test"
