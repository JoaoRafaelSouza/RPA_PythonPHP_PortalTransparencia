import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_buscar_cpf():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"cpf": "12345678901"}
        response = await ac.post("/api/buscar", json=payload)
        assert response.status_code == 200
        assert "resultado" in response.json()

@pytest.mark.asyncio
async def test_buscar_nome():
    payload = {"nome": "João"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/buscar", json=payload)
        assert response.status_code == 200