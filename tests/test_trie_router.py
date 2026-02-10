from microapi.router.trie import TrieRouter


async def handler_a(request):
    return "a"


async def handler_b(request):
    return "b"


def test_static_route_match():
    router = TrieRouter()
    router.add("GET", "/health", handler_a)

    result = router.match("GET", "/health")

    assert result is not None

    handler, params = result
    assert handler is handler_a
    assert params == {}


def test_dynamic_route_match():
    router = TrieRouter()
    router.add("GET", "/users/{id}", handler_a)

    result = router.match("GET", "/users/123")

    assert result is not None

    handler, params = result
    assert handler is handler_a
    assert params == {"id": "123"}


def test_static_precedence_over_dynamic():
    router = TrieRouter()
    router.add("GET", "/users/{id}", handler_a)
    router.add("GET", "/users/me", handler_b)

    result = router.match("GET", "/users/me")

    assert result is not None

    handler, params = result
    assert handler is handler_b
    assert params == {}


def test_method_mismatch_returns_none():
    router = TrieRouter()
    router.add("GET", "/users/{id}", handler_a)

    result = router.match("POST", "/users/123")

    assert result is None


def test_unknown_path_returns_none():
    router = TrieRouter()

    result = router.match("GET", "/does-not-exist")

    assert result is None
