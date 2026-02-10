from microapi.core.exceptions import HTTPException
from microapi.core.request import Request
from microapi.core.response import Response
from microapi.core.router import BaseRouter
from microapi.introspection import render_endpoints_page
from microapi.request.asgi import ASGIRequest
from microapi.response import JSONResponse, TextResponse
from microapi.router.simple import SimpleRouter


class MicroAPI:
    def __init__(self, router: BaseRouter | None = None):
        self.router = router or SimpleRouter()

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return

        request: Request = ASGIRequest(scope, receive)

        if request.method == "GET" and request.path == "/__endpoints__":
            html = render_endpoints_page(self.router)
            response = TextResponse(html)
            response.headers["content-type"] = "text/html; charset=utf-8"
            await response.send(send)
            return

        if request.method == "OPTIONS":
            allowed = None
            if hasattr(self.router, "allowed_methods"):
                allowed = self.router.allowed_methods(request.path)

            if allowed:
                response = TextResponse(
                    "",
                    status_code=200,
                    headers={"allow": ", ".join(sorted(allowed))},
                )
                await response.send(send)
                return

        match = self.router.match(request.method, request.path)

        if match is None:
            allowed = None
            if hasattr(self.router, "allowed_methods"):
                allowed = self.router.allowed_methods(request.path)

            if allowed:
                # Path exists, method not allowed
                response = TextResponse(
                    "Method Not Allowed",
                    status_code=405,
                    headers={"allow": ", ".join(sorted(allowed))},
                )
            else:
                # Path does not exist
                response = TextResponse("Not Found", status_code=404)

            await response.send(send)
            return

        handler, path_params = match
        request.path_params.update(path_params)

        try:
            result = await handler(request)
        except HTTPException as exc:
            response = JSONResponse(
                {"detail": exc.detail},
                status_code=exc.status_code,
                headers=exc.headers,
            )
            await response.send(send)
            return

        if isinstance(result, Response):
            response = result
        elif isinstance(result, dict):
            response = JSONResponse(result)
        elif isinstance(result, str):
            response = TextResponse(result)
        else:
            response = TextResponse(str(result))

        await response.send(send)


app = MicroAPI()
