import inspect
from typing import Any

from microapi.dependencies import Depends


async def resolve_dependencies(func, request, registry, request_cache, teardown_stack):
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
                teardown_stack,
            )

        elif name == "request":
            values[name] = request

    return values


async def _resolve_dependency(dep, request, registry, request_cache, teardown_stack):
    if isinstance(dep, str):
        return registry.resolve(dep, request_cache)

    if dep in request_cache:
        return request_cache[dep]

    kwargs = await resolve_dependencies(
        dep,
        request,
        registry,
        request_cache,
        teardown_stack,
    )

    if inspect.isasyncgenfunction(dep):
        agen = dep(**kwargs)
        value = await agen.__anext__()
        teardown_stack.append(agen)
    else:
        if "request" in inspect.signature(dep).parameters:
            result = dep(request, **kwargs)
        else:
            result = dep(**kwargs)

        if inspect.isawaitable(result):
            result = await result

        value = result

    request_cache[dep] = value
    return value
