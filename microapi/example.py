from microapi.app import app


async def ping():
    return "pong"


async def hello():
    return "hello world"


app.router.add("GET", "/ping", ping)
app.router.add("GET", "/hello", hello)
