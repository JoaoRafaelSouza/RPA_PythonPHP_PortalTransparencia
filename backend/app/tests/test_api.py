import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from main import app

@pytest.mark.asyncio
async def test_buscar_cpf():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {"cpf": "12345678901"}
        response = await ac.post("/api/buscar", json=payload)
        assert response.status_code == 200
        assert "resultado" in response.json()

@pytest.mark.asyncio
async def test_buscar_nome():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {"nome": "João"}
        response = await ac.post("/api/buscar", json=payload)
        assert response.status_code == 200