import inspect
from typing import Any

from microapi.background import BackgroundTasks
from microapi.dependencies import Depends


async def resolve_dependencies(
    func,
    request,
    registry,
    request_cache,
    teardown_stack,
    overrides=None,
):
    overrides = overrides or {}
    sig = inspect.signature(func)
    values: dict[str, Any] = {}

    for name, param in sig.parameters.items():
        default = param.default

        if param.annotation is BackgroundTasks:
            values[name] = BackgroundTasks()

        elif isinstance(default, Depends):
            values[name] = await _resolve_dependency(
                default.dependency,
                request,
                registry,
                request_cache,
                teardown_stack,
                overrides,
            )

        elif name == "request":
            values[name] = request

    return values


async def _resolve_dependency(
    dep,
    request,
    registry,
    request_cache,
    teardown_stack,
    overrides,
):
    if dep in overrides:
        dep = overrides[dep]

    if isinstance(dep, str):
        if dep in overrides:
            dep = overrides[dep]
            return dep()
        return registry.resolve(dep, request_cache)

    if dep in request_cache:
        return request_cache[dep]

    kwargs = await resolve_dependencies(
        dep,
        request,
        registry,
        request_cache,
        teardown_stack,
        overrides,
    )

    if inspect.isasyncgenfunction(dep):
        agen = dep(**kwargs)
        value = await agen.__anext__()
        teardown_stack.append(agen)
    else:
        value = dep(**kwargs)
        if inspect.isawaitable(value):
            value = await value

    request_cache[dep] = value
    return value
