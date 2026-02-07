from typing import Awaitable, Callable, Dict, List, NewType

Handler = Callable[..., Awaitable[object]]
HeaderName = NewType("HeaderName", str)
HeaderValue = NewType("HeaderValue", str)
QueryParams = Dict[str, List[str]]
