import pytest
from fastapi import FastAPI
from httpx import AsyncClient


class TestAuth:
    @pytest.mark.asyncio
    async def test_register(
            self,
            async_client: AsyncClient,
            app: FastAPI,
    ):
        response = await async_client.post(app.url_path_for("auth:register"),
                                           json={"email": "admin@admin.com", "password": "Atabak1234",
                                                 "re_password": "Atabak1234"})

        assert response.status_code == 201
        assert "token" in response.json()['result']

    @pytest.mark.asyncio
    async def test_login_with_wrong_password(
            self,
            async_client: AsyncClient,
            app: FastAPI
    ):
        response = await async_client.post(app.url_path_for("auth:login"),
                                           json={"email": "admin@admin.com", "password": "Atabak12345"})

        assert response.status_code == 401
        assert response.json()['result'] == 'Invalid credentials'

    @pytest.mark.asyncio
    async def test_login(
            self,
            async_client: AsyncClient,
            app: FastAPI
    ):
        response = await async_client.post(app.url_path_for("auth:login"),
                                           json={"email": "admin@admin.com", "password": "Atabak1234"})

        assert response.status_code == 200
        assert "token" in response.json()['result']
