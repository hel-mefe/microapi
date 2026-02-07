from microapi.core.response import Response


class TextResponse(Response):
    """
    Plain text HTTP response.
    """

    def __init__(
        self,
        content: str,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
    ):
        super().__init__(status_code=status_code, headers=headers)
        self._body = content.encode("utf-8")
        self.headers.setdefault(
            "content-type",
            "text/plain; charset=utf-8",
        )

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
                "body": self._body,
            }
        )

