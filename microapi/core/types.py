from typing import Awaitable, Callable, NewType

Handler = Callable[..., Awaitable[object]]
HeaderName = NewType("HeaderName", str)
HeaderValue = NewType("HeaderValue", str)


