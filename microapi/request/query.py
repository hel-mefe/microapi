from collections.abc import Mapping
from urllib.parse import parse_qs

from microapi.core.types import QueryParams


class QueryParamsView(Mapping[str, list[str]]):
    def __init__(self, raw: bytes):
        self._data: QueryParams = parse_qs(raw.decode("utf-8"), keep_blank_values=True)

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def __getitem__(self, key: str) -> list[str]:
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)
