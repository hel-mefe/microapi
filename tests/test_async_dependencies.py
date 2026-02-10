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
async def test_async_generator_dependency_setup_and_teardown():
    events = []

    async def get_resource():
        events.append("setup")
        yield "resource"
        events.append("teardown")

    async def handler(res=Depends(get_resource)):
        return res

    router = TrieRouter()
    router.add("GET", "/", handler)

    app = MicroAPI(router)

    send = SendCollector()
    await app(make_scope(), None, send)

    assert send.messages[1]["body"] == b"resource"
    assert events == ["setup", "teardown"]


@pytest.mark.asyncio
async def test_async_generator_teardown_on_exception():
    events = []

    async def get_resource():
        events.append("setup")
        yield "resource"
        events.append("teardown")

    async def handler(res=Depends(get_resource)):
        raise RuntimeError("boom")

    router = TrieRouter()
    router.add("GET", "/", handler)

    app = MicroAPI(router)

    send = SendCollector()
    await app(make_scope(), None, send)

    assert events == ["setup", "teardown"]
