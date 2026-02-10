from collections.abc import Awaitable, Callable
from typing import NewType

Handler = Callable[..., Awaitable[object]]
HeaderName = NewType("HeaderName", str)
HeaderValue = NewType("HeaderValue", str)
QueryParams = dict[str, list[str]]
