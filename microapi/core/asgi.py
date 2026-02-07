from typing import Any, Awaitable, Callable, Dict

Scope = Dict[str, Any]

Receive = Callable[
    [],
    Awaitable[Dict[str, Any]],
]

Send = Callable[
    [Dict[str, Any]],
    Awaitable[None],
]


