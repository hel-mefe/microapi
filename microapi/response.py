from microapi.core.router import BaseRouter
from microapi.router.simple import SimpleRouter
from microapi.request import Request
from microapi.response import TextResponse, JSONResponse
from microapi.core.response import Response


class MicroAPI:
    def __init__(self, router: BaseRouter | None = None):
        self.router = router or SimpleRouter()

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return

        request = Request(scope, receive)
        handler = self.router.match(request.method, request.path)

        if handler is None:
            response = TextResponse("Not Found", status_code=404)
            await response.send(send)
            return

        result = await handler(request)

        if isinstance(result, Response):
            response = result
        elif isinstance(result, dict):
            response = JSONResponse(result)
        elif isinstance(result, str):
            response = TextResponse(result)
        else:
            response = TextResponse(str(result))

        await response.send(send)

