import inspect
from typing import Any

from microapi.dependencies import Depends


async def resolve_dependencies(func, request, registry, request_cache) -> dict[str, Any]:
    sig = inspect.signature(func)
    values: dict[str, Any] = {}

    for name, param in sig.parameters.items():
        default = param.default

        if isinstance(default, Depends):
            dep = default.dependency

            if isinstance(dep, str):
                value = registry.resolve(dep, request_cache)
            else:
                if "request" in inspect.signature(dep).parameters:
                    value = dep(request)
                else:
                    value = dep()

                if inspect.isawaitable(value):
                    value = await value

            values[name] = value

        elif name == "request":
            values[name] = request

    return values
