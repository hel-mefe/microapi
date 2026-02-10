import time

from microapi.core.request import Request
from microapi.core.response import Response


class LoggingMiddleware:
    async def __call__(self, request: Request, call_next) -> Response:
        start = time.perf_counter()

        response = await call_next(request)

        duration = (time.perf_counter() - start) * 1000
        method = request.method
        path = request.path
        status = response.status_code

        print(f"{method} {path} -> {status} ({duration:.2f}ms)")

        return response
