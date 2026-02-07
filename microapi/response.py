import json
from typing import Any

from microapi.core.response import Response


class TextResponse(Response):
    def __init__(
        self,
        content: str,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
    ):
        super().__init__(status_code, headers)
        self.body = content.encode("utf-8")
        self.headers.setdefault("content-type", "text/plain; charset=utf-8")

    async def send(self, send) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": [
                    (k.encode("latin-1"), v.encode("latin-1"))
                    for k, v in self.headers.items()
                ],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": self.body,
            }
        )


class JSONResponse(Response):
    def __init__(
        self,
        content: Any,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
    ):
        super().__init__(status_code, headers)
        self.body = json.dumps(content).encode("utf-8")
        self.headers.setdefault("content-type", "application/json")

    async def send(self, send) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": [
                    (k.encode("latin-1"), v.encode("latin-1"))
                    for k, v in self.headers.items()
                ],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": self.body,
            }
        )

