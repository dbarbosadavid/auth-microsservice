import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pytest
from fastapi.testclient import TestClient

from app import app  


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def access_token():
    with TestClient(app) as client:
        response = client.post("/token/auth", json={
            "email": "teste@teste.com",
            "password": "12345678"
        })
        access_token = response.json()["access_token"]
        yield access_token

@pytest.fixture
def new_access_token():
    with TestClient(app) as client:
        response = client.post("/token/auth", json={
            "email": "teste@teste.com",
            "password": "newpassword123"
        })
        new_access_token = response.json()["access_token"]
        yield new_access_token