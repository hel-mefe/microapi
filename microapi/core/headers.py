from typing import Iterator, Mapping, Optional, List, Tuple
from .types import HeaderName, HeaderValue

ASGIHeaders = List[Tuple[bytes, bytes]]

class HeadersView(Mapping[str, str]):
    """
    Read-only, case-insensitive HTTP headers.

    This is a value object:
    - No mutation
    - No side effects
    - No parsing beyond decoding
    """

    def __init__(self, raw: ASGIHeaders):
        self._headers: dict[HeaderName, HeaderValue] = {}

        for key, value in raw:
            name = HeaderName(key.decode("latin-1").lower())
            val = HeaderValue(value.decode("latin-1"))
            self._headers[name] = val

    def __getitem__(self, key: str) -> str:
        return self._headers[HeaderName(key.lower())]

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return self._headers.get(HeaderName(key.lower()), default)

    def __iter__(self) -> Iterator[str]:
        return (k for k in self._headers)

    def __len__(self) -> int:
        return len(self._headers)

