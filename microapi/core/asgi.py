from collections.abc import Awaitable, Callable
from typing import Any

Scope = dict[str, Any]

Receive = Callable[
    [],
    Awaitable[dict[str, Any]],
]

Send = Callable[
    [dict[str, Any]],
    Awaitable[None],
]
