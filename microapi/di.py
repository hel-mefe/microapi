import inspect
from typing import Any

from microapi.dependencies import Depends


async def resolve_dependencies(func, request, registry, request_cache) -> dict[str, Any]:
    sig = inspect.signature(func)
    values: dict[str, Any] = {}

    for name, param in sig.parameters.items():
        default = param.default

        if isinstance(default, Depends):
            values[name] = await _resolve_dependency(
                default.dependency,
                request,
                registry,
                request_cache,
            )

        elif name == "request":
            values[name] = request

    return values


async def _resolve_dependency(dep, request, registry, request_cache):
    if isinstance(dep, str):
        return registry.resolve(dep, request_cache)

    if dep in request_cache:
        return request_cache[dep]

    kwargs = await resolve_dependencies(dep, request, registry, request_cache)

    if "request" in inspect.signature(dep).parameters:
        result = dep(request, **kwargs)
    else:
        result = dep(**kwargs)

    if inspect.isawaitable(result):
        result = await result

    request_cache[dep] = result
    return result
