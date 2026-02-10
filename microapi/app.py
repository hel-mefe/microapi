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


class MicroAPI:
    def __init__(self, router: BaseRouter | None = None):
        self.router = router or SimpleRouter()
        self.registry = Registry()
        self._middlewares = []

    def add_middleware(self, middleware):
        self._middlewares.append(middleware)

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return

        request: Request = ASGIRequest(scope, receive)

        async def app_handler(request):
            if request.method == "GET" and request.path == "/__endpoints__":
                html = render_endpoints_page(self.router)
                response = TextResponse(html)
                response.headers["content-type"] = "text/html; charset=utf-8"
                return response

            match = self.router.match(request.method, request.path)

            if match is None:
                allowed = self.router.allowed_methods(request.path)
                if allowed:
                    response = TextResponse(
                        "Method Not Allowed",
                        status_code=405,
                        headers={"allow": ", ".join(sorted(allowed))},
                    )
                else:
                    response = TextResponse("Not Found", status_code=404)
                return response

            handler, path_params = match
            request.path_params = path_params

            teardown_stack = []
            request_cache = {}

            try:
                kwargs = await resolve_dependencies(
                    handler,
                    request,
                    self.registry,
                    request_cache,
                    teardown_stack,
                )
                result = await handler(**kwargs)
            except HTTPException as exc:
                response = JSONResponse(
                    {"detail": exc.detail},
                    status_code=exc.status_code,
                    headers=exc.headers,
                )
            except Exception:
                response = TextResponse("Internal Server Error", status_code=500)
            else:
                if isinstance(result, Response):
                    response = result
                elif isinstance(result, dict):
                    response = JSONResponse(result)
                elif isinstance(result, str):
                    response = TextResponse(result)
                else:
                    response = TextResponse(str(result))
            finally:
                for agen in reversed(teardown_stack):
                    try:
                        await agen.__anext__()
                    except StopAsyncIteration:
                        pass

            return response

        handler = app_handler
        for middleware in reversed(self._middlewares):
            next_handler = handler

            async def handler(request, middleware=middleware, next_handler=next_handler):
                return await middleware(request, next_handler)

        response = await handler(request)
        await response.send(send)


app = MicroAPI()
