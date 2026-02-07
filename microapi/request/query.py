from urllib.parse import parse_qs
from typing import Mapping, List
from microapi.core.types import QueryParams

class QueryParamsView(Mapping[str, List[str]]):
    def __init__(self, raw: bytes):
        self._data: QueryParams = parse_qs(raw.decode("utf-8"), keep_blank_values=True)

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def __getitem__(self, key: str) -> List[str]:
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)
