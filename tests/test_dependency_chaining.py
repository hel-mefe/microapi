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
async def test_dependency_chaining():
    async def get_db():
        return "db"

    async def get_user(db=Depends(get_db)):
        return f"user-from-{db}"

    async def handler(user=Depends(get_user)):
        return user

    router = TrieRouter()
    router.add("GET", "/", handler)

    app = MicroAPI(router)

    send = SendCollector()
    await app(make_scope(), None, send)

    assert send.messages[1]["body"] == b"user-from-db"


@pytest.mark.asyncio
async def test_dependency_cached_per_request():
    calls = []

    async def get_db():
        calls.append("db")
        return "db"

    async def get_user(db=Depends(get_db)):
        return db

    async def handler(
        u1=Depends(get_user),
        u2=Depends(get_user),
    ):
        return f"{u1}-{u2}"

    router = TrieRouter()
    router.add("GET", "/", handler)

    app = MicroAPI(router)

    send = SendCollector()
    await app(make_scope(), None, send)

    assert calls == ["db"]
    assert send.messages[1]["body"] == b"db-db"
