from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.tron.schemas import TronLogPydantic


client = TestClient(app)


def test_healthcheck():
    response = client.get("/")
    data = response.json()
    assert data == {"status": "ok"}


def test_post_info_endpoint_error():
    response = client.post("/tron/info", json={"address": "NHWckSxxzHbJgMeUaYin4ABMcLvmWiPz"})
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["type"] == "value_error"


mocked_info = {
    "address": "T1234567890abcdef",
    "balance": 1000,
    "bandwidth": 5000,
    "energy": 10000
}


@pytest.fixture
def mock_add_address():
    with patch("app.api.router.add_address", new_callable=AsyncMock) as mock_func:
        mock_func.return_value = TronLogPydantic(**mocked_info)
        yield mock_func

def test_post_info_endpoint_success(mock_add_address):
    response = client.post("/tron/info", json={"address": "T1234567890abcdef"})
    assert response.status_code == 200
    data = response.json()
    assert data["address"] == "T1234567890abcdef"
    assert data["balance"] == 1000


mocked_history = [
    {
        "address": "T1234567890abcdef",
        "balance": 1000,
        "bandwidth": 5000,
        "energy": 10000
    },
    {
        "address": "T9876543210fedcba",
        "balance": 2500,
        "bandwidth": 3000,
        "energy": 8000
    },
    {
        "address": "T1A2B3C4D5E6F7G8H9",
        "balance": 500,
        "bandwidth": 10000,
        "energy": 2000
    }
]

@pytest.fixture
def mock_extract():
    with patch("app.api.router.extract_latest", new_callable=AsyncMock) as mock_func:
        mock_func.return_value = [TronLogPydantic(**inst) for inst in mocked_history]
        yield mock_func


def test_get_history(mock_extract):
    response = client.get("/tron/history")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["address"] == "T1234567890abcdef"
    assert data[1]["energy"] == 8000
    assert data[2]["balance"] == 500
