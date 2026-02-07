class MicroAPI:
    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return

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


app = MicroAPI()
