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
async def test_app_get_decorator():
    app = MicroAPI()

    @app.get("/ping")
    async def ping():
        return "pong"

    send = SendCollector()
    await app(make_scope(path="/ping"), None, send)

    assert send.messages[1]["body"] == b"pong"


@pytest.mark.asyncio
async def test_router_post_decorator():
    router = TrieRouter()

    @router.post("/submit")
    async def submit():
        return "ok"

    app = MicroAPI(router)

    send = SendCollector()
    await app(make_scope(method="POST", path="/submit"), None, send)

    assert send.messages[1]["body"] == b"ok"


@pytest.mark.asyncio
async def test_decorator_respects_http_method():
    app = MicroAPI()

    @app.get("/only-get")
    async def handler():
        return "ok"

    send = SendCollector()
    await app(make_scope(method="POST", path="/only-get"), None, send)

    assert send.messages[0]["status"] == 405
