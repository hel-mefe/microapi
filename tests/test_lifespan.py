import pytest

from microapi.app import MicroAPI


@pytest.mark.asyncio
async def test_startup_and_shutdown_hooks_run():
    events = []

    app = MicroAPI()

    @app.on_startup
    async def startup():
        events.append("startup")

    @app.on_shutdown
    async def shutdown():
        events.append("shutdown")

    await app._run_startup()
    await app._run_shutdown()

    assert events == ["startup", "shutdown"]


@pytest.mark.asyncio
async def test_multiple_hooks_preserve_order():
    events = []

    app = MicroAPI()

    @app.on_startup
    async def s1():
        events.append("s1")

    @app.on_startup
    async def s2():
        events.append("s2")

    @app.on_shutdown
    async def d1():
        events.append("d1")

    @app.on_shutdown
    async def d2():
        events.append("d2")

    await app._run_startup()
    await app._run_shutdown()

    assert events == ["s1", "s2", "d1", "d2"]
