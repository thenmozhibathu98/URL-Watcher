import asyncio
import pytest
from httpx import AsyncClient
from app.main import app
from app. db import init_db
import os
os.environ["DISABLE_WATCHER"] = "1"

@pytest.fixture(autouse=True)
def init():
    dbfile = "./data.db"
    try:
        os.remove(dbfile)
    except Exception:
        pass
    init_db()
    yield
    try:
        os.remove(dbfile)
    except Exception: 
        pass


@pytest.mark. asyncio
async def test_create_and_get_checks():
    async with AsyncClient(app=app, base_url="http://test") as client:
        resp = await client.post("/urls", json={"url": "https://httpbin.org/get", "interval": 1})
        assert resp.status_code == 201
        data = resp.json()
        url_id = data["id"]

        resp2 = await client.post(f"/urls/{url_id}/trigger")
        assert resp2.status_code == 202

        await asyncio.sleep(2)

        resp3 = await client.get(f"/urls/{url_id}/checks")
        assert resp3.status_code == 200
        checks = resp3.json()
        assert len(checks) >= 1
        assert any(c["success"] is True for c in checks)
