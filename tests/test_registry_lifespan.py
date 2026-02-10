import pytest

from microapi.app import MicroAPI


@pytest.mark.asyncio
async def test_app_scoped_registry_lifecycle():
    events = []

    def create_resource():
        events.append("create")
        return {"value": 42}

    async def on_startup():
        events.append("startup")

    async def on_shutdown(resource):
        events.append("shutdown")

    app = MicroAPI()

    app.registry.register(
        "resource",
        create_resource,
        scope="app",
        on_startup=on_startup,
        on_shutdown=on_shutdown,
    )

    await app._run_startup()
    await app._run_shutdown()

    assert events == ["startup", "create", "shutdown"]
