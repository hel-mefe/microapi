from microapi.background import BackgroundTasks
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

        self._startup_handlers = []
        self._shutdown_handlers = []
        self._started = False

        self.dependency_overrides = {}

    def add_middleware(self, middleware):
        self._middlewares.append(middleware)

    def on_startup(self, func):
        self._startup_handlers.append(func)
        return func

    def on_shutdown(self, func):
        self._shutdown_handlers.append(func)
        return func

    async def _run_startup(self):
        if self._started:
            return
        for func in self._startup_handlers:
            result = func()
            if hasattr(result, "__await__"):
                await result
        await self.registry.startup()
        self._started = True

    async def _run_shutdown(self):
        if not self._started:
            return
        await self.registry.shutdown()
        for func in self._shutdown_handlers:
            result = func()
            if hasattr(result, "__await__"):
                await result
        self._started = False

    def route(self, path: str, method: str):
        return self.router.route(path, method)

    def get(self, path: str):
        return self.router.get(path)

    def post(self, path: str):
        return self.router.post(path)

    def put(self, path: str):
        return self.router.put(path)

    def delete(self, path: str):
        return self.router.delete(path)

    def patch(self, path: str):
        return self.router.patch(path)

    async def __call__(self, scope, receive, send):
        if scope["type"] == "lifespan":
            message = await receive()
            if message["type"] == "lifespan.startup":
                await self._run_startup()
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                await self._run_shutdown()
                await send({"type": "lifespan.shutdown.complete"})
            return

        if scope["type"] != "http":
            return

        await self._run_startup()

        request: Request = ASGIRequest(scope, receive)

        async def app_handler(request: Request) -> Response:
            if request.method == "GET" and request.path == "/__endpoints__":
                html = render_endpoints_page(self.router)
                response = TextResponse(html)
                response.headers["content-type"] = "text/html; charset=utf-8"
                return response

            match = self.router.match(request.method, request.path)
            if match is None:
                allowed = self.router.allowed_methods(request.path)
                if allowed:
                    return TextResponse(
                        "Method Not Allowed",
                        status_code=405,
                        headers={"allow": ", ".join(sorted(allowed))},
                    )
                return TextResponse("Not Found", status_code=404)

            handler, path_params = match
            request.path_params = path_params

            teardown_stack = []
            request_cache = {}

            background_tasks = None

            try:
                kwargs = await resolve_dependencies(
                    handler,
                    request,
                    self.registry,
                    request_cache,
                    teardown_stack,
                    self.dependency_overrides,
                )

                for value in kwargs.values():
                    if isinstance(value, BackgroundTasks):
                        background_tasks = value
                        break

                result = await handler(**kwargs)

            except HTTPException as exc:
                return JSONResponse(
                    {"detail": exc.detail},
                    status_code=exc.status_code,
                    headers=exc.headers,
                )
            except Exception:
                return TextResponse("Internal Server Error", status_code=500)
            finally:
                for agen in reversed(teardown_stack):
                    try:
                        await agen.__anext__()
                    except StopAsyncIteration:
                        pass

            if isinstance(result, Response):
                response = result
            elif isinstance(result, dict):
                response = JSONResponse(result)
            elif isinstance(result, str):
                response = TextResponse(result)
            else:
                response = TextResponse(str(result))

            response._background_tasks = background_tasks
            return response

        handler = app_handler
        for middleware in reversed(self._middlewares):
            next_handler = handler

            async def handler(request, middleware=middleware, next_handler=next_handler):
                return await middleware(request, next_handler)

        response = await handler(request)

        await response.send(send)

        background_tasks = getattr(response, "_background_tasks", None)
        if background_tasks:
            await background_tasks.run()


app = MicroAPI()
