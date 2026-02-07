from router import Router

class MicroAPI:

    def __init__(self):
        self.router = Router()

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return

        method, path = scope['method'], scope['path']
        handler = self.router.match(method, path)

        print('METHOD => ', method)
        print('PATH => ', path)
        print('HANDLER -> ', handler)

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
