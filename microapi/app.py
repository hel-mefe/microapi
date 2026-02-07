from microapi.router import SimpleRouter
from microapi.core import BaseRouter

class MicroAPI:

    def __init__(self, router: BaseRouter | None = None):
        """
            @constructor params
             - router: a concrete implementation for abstract class BaseRouter,
             if not provided then falls back to SimpleRouter instance
        """
        self.router = router or SimpleRouter()

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return

        method, path = scope['method'], scope['path']
        handler = self.router.match(method, path)

        if handler is None:
            await send(
                {
                    "type": "http.response.start",
                    "status": 200,
                    "headers": [
                        (b"content-type", b"text/plain"),
                    ],
                }
            )

            await send(
                {
                    "type": "http.response.body",
                    "body": b"Hello from MicroAPI",
                }
            )
            return

        result = await handler()
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [(b"content-type", b"text/plain")],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": result.encode(),
            }
        )


app = MicroAPI()
