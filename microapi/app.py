from collections.abc import Awaitable, Callable

from microapi.core.exceptions import HTTPException
from microapi.core.request import Request
from microapi.core.response import Response
from microapi.core.router import BaseRouter
from microapi.di import resolve_dependencies
from microapi.introspection import render_endpoints_page
from microapi.registry import Registry
from microapi.request.asgi import ASGIRequest
from microapi.response import JSONResponse, TextResponse
from microapi.router.simple import SimpleRouter

Middleware = Callable[
    [Request, Callable[[Request], Awaitable[Response]]],
    Awaitable[Response],
]


class MicroAPI:
    def __init__(self, router: BaseRouter | None = None):
        self.router = router or SimpleRouter()
        self._middleware: list[Middleware] = []
        self.registry = Registry()

    def add_middleware(self, middleware: Middleware) -> None:
        self._middleware.append(middleware)

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return

        request: Request = ASGIRequest(scope, receive)

        handler = self._handle_request
        for middleware in reversed(self._middleware):
            next_handler = handler

            async def handler(request, mw=middleware, nxt=next_handler):
                return await mw(request, nxt)

        response = await handler(request)
        await response.send(send)

    async def _handle_request(self, request: Request) -> Response:
        if request.method == "GET" and request.path == "/__endpoints__":
            html = render_endpoints_page(self.router)
            response = TextResponse(html)
            response.headers["content-type"] = "text/html; charset=utf-8"
            return response

        if request.method == "OPTIONS":
            allowed = None
            if hasattr(self.router, "allowed_methods"):
                allowed = self.router.allowed_methods(request.path)

            if allowed:
                return TextResponse(
                    "",
                    status_code=200,
                    headers={"allow": ", ".join(sorted(allowed))},
                )

        match = self.router.match(request.method, request.path)

        if match is None:
            allowed = None
            if hasattr(self.router, "allowed_methods"):
                allowed = self.router.allowed_methods(request.path)

            if allowed:
                return TextResponse(
                    "Method Not Allowed",
                    status_code=405,
                    headers={"allow": ", ".join(sorted(allowed))},
                )

            return TextResponse("Not Found", status_code=404)

        handler, path_params = match
        request.path_params.update(path_params)

        request_cache: dict[str, object] = {}

        try:
            kwargs = await resolve_dependencies(
                handler,
                request,
                self.registry,
                request_cache,
            )
            result = await handler(**kwargs)
        except HTTPException as exc:
            return JSONResponse(
                {"detail": exc.detail},
                status_code=exc.status_code,
                headers=exc.headers,
            )

        if isinstance(result, Response):
            return result
        if isinstance(result, dict):
            return JSONResponse(result)
        if isinstance(result, str):
            return TextResponse(result)

        return TextResponse(str(result))


app = MicroAPI()
