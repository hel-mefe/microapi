import inspect
from collections.abc import Callable
from typing import Any


class BackgroundTasks:
    def __init__(self):
        self._tasks: list[tuple[Callable[..., Any], tuple, dict]] = []

    def add(self, func: Callable[..., Any], *args, **kwargs):
        self._tasks.append((func, args, kwargs))

    async def run(self):
        for func, args, kwargs in self._tasks:
            try:
                result = func(*args, **kwargs)
                if inspect.isawaitable(result):
                    await result
            except Exception:
                pass
