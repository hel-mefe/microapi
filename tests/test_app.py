import pytest

from microapi.app import MicroAPI
from microapi.router.trie import TrieRouter
from microapi.core.exceptions import HTTPException


class SendCollector:
    """
    Collects ASGI send() messages for inspection.
    """
    def __init__(self):
        self.messages = []

    async def __call__(self, message):
        self.messages.append(message)


def make_scope(method: str = "GET", path: str = "/"):
    """
    Create a minimal ASGI HTTP scope.
    """
    return {
        "type": "http",
        "method": method,
        "path": path,
        "raw_path": path.encode(),
        "query_string": b"",
        "headers": [],
    }


@pytest.mark.asyncio
async def test_app_returns_text_response():
    router = TrieRouter()

    async def handler(request):
        return "hello"

    router.add("GET", "/", handler)
    app = MicroAPI(router)

    send = SendCollector()
    scope = make_scope()

    await app(scope, receive=None, send=send)

    assert len(send.messages) == 2
    assert send.messages[0]["type"] == "http.response.start"
    assert send.messages[1]["type"] == "http.response.body"
    assert send.messages[1]["body"] == b"hello"


@pytest.mark.asyncio
async def test_app_returns_json_response():
    router = TrieRouter()

    async def handler(request):
        return {"message": "ok"}

    router.add("GET", "/", handler)
    app = MicroAPI(router)

    send = SendCollector()
    scope = make_scope()

    await app(scope, receive=None, send=send)

    assert send.messages[1]["body"] == b'{"message": "ok"}'


@pytest.mark.asyncio
async def test_path_params_injected_into_request():
    router = TrieRouter()

    async def handler(request):
        return request.path_params["id"]

    router.add("GET", "/users/{id}", handler)
    app = MicroAPI(router)

    send = SendCollector()
    scope = make_scope(path="/users/42")

    await app(scope, receive=None, send=send)

    assert send.messages[1]["body"] == b"42"


@pytest.mark.asyncio
async def test_app_returns_404_for_unknown_path():
    router = TrieRouter()
    app = MicroAPI(router)

    send = SendCollector()
    scope = make_scope(path="/unknown")

    await app(scope, receive=None, send=send)

    assert send.messages[0]["status"] == 404


@pytest.mark.asyncio
async def test_http_exception_is_handled_by_framework():
    router = TrieRouter()

    async def handler(request):
        raise HTTPException(400, "bad request")

    router.add("GET", "/", handler)
    app = MicroAPI(router)

    send = SendCollector()
    scope = make_scope()

    await app(scope, receive=None, send=send)

    assert send.messages[0]["status"] == 400
    assert b"bad request" in send.messages[1]["body"]

