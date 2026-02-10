import pytest

from microapi.app import MicroAPI
from microapi.middleware.cors import CORSMiddleware
from microapi.router.trie import TrieRouter


class SendCollector:
    def __init__(self):
        self.messages = []

    async def __call__(self, message):
        self.messages.append(message)


def make_scope(method="GET", path="/", headers=None):
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
async def test_cors_credentials_sets_allow_credentials():
    async def handler(request):
        return "ok"

    router = TrieRouter()
    router.add("GET", "/", handler)

    app = MicroAPI(router)
    app.add_middleware(
        CORSMiddleware(
            allow_origins=["http://example.com"],
            allow_credentials=True,
        )
    )

    send = SendCollector()
    scope = make_scope(headers={"Origin": "http://example.com"})

    await app(scope, receive=None, send=send)

    headers = dict(send.messages[0]["headers"])
    assert headers[b"access-control-allow-origin"] == b"http://example.com"
    assert headers[b"access-control-allow-credentials"] == b"true"


@pytest.mark.asyncio
async def test_cors_credentials_rejects_wildcard_origin():
    with pytest.raises(ValueError):
        CORSMiddleware(
            allow_origins=["*"],
            allow_credentials=True,
        )
