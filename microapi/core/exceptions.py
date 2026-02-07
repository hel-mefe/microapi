class HTTPException(Exception):
    """
    Base HTTP exception.

    Used to interrupt normal handler execution
    and return a specific HTTP response.
    """

    def __init__(self, status_code: int, detail: str | None = None, headers: dict[str, str] | None = None):
        self.status_code = status_code
        self.detail = detail or ""
        self.headers = headers or {}
        super().__init__(detail)

