from microapi.core.exceptions import HTTPException

class NotFound(HTTPException):
    def __init__(self, detail: str = "Not Found"):
        super().__init__(404, detail)

class BadRequest(HTTPException):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(400, detail)

class Unauthorized(HTTPException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(401, detail)


class Forbidden(HTTPException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(403, detail)
