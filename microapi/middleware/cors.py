from microapi.core.request import Request
from microapi.core.response import Response
from microapi.response import TextResponse


class CORSMiddleware:
    """ "
    L middleware khasso bdarroura ykon callable, that's important

    in addition to that, kaynin parameters to customize cors

    - allow_origins: origins li can send us a request
    - allow_methods: methods li we allow
    - allow_headers: headers li we allow

    User dial microapi is supposed y setti credentials

    Note: by default we allow all origins, all methods, all headers

    """

    def __init__(self, allow_origins=None, allow_methods=None, allow_headers=None):
        self.allow_origins = allow_origins or ["*"]
        self.allow_methods = allow_methods or [
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
            "OPTIONS",
        ]
        self.allow_headers = allow_headers or ["*"]

    async def __call__(self, request: Request, call_next) -> Response:
        origin = request.headers.get("origin")

        if not origin:
            return await call_next(request)

        if request.method == "OPTIONS":
            response = TextResponse("", status_code=200)
        else:
            response = await call_next(request)

        self._set_cors_headers(response, origin)
        return response

    def _set_cors_headers(self, response: Response, origin: str) -> None:
        if "*" in self.allow_origins:
            response.headers["access-control-allow-origin"] = "*"
        elif origin in self.allow_origins:
            response.headers["access-control-allow-origin"] = origin

        response.headers["access-control-allow-methods"] = ", ".join(self.allow_methods)

        response.headers["access-control-allow-headers"] = ", ".join(self.allow_headers)
