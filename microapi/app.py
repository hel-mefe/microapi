from microapi.core.router import BaseRouter
from microapi.router.simple import SimpleRouter
from microapi.core.request import Request
from microapi.request.asgi import ASGIRequest
from microapi.response import TextResponse, JSONResponse
from microapi.core.response import Response
from microapi.core.exceptions import HTTPException
from microapi.introspection import render_endpoints_page
from microapi.response import TextResponse

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

        handler = self.router.match(request.method, request.path)
        if handler is None:
            response = TextResponse("Not Found", status_code=404)
            await response.send(send)
            return

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
