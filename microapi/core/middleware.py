from collections.abc import Awaitable, Callable

from microapi.core.request import Request
from microapi.core.response import Response

Middleware = Callable[
    [Request, Callable[[Request], Awaitable[Response]]],
    Awaitable[Response],
]
