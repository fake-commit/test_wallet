import pytest
from rest_framework.test import APIClient
from .models import Wallet


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def wallet():
    return Wallet.objects.create(label="Test Wallet", balance=0)


@pytest.mark.django_db
def test_create_wallet(api_client):
    data = {
        "data": {
            "type": "Wallet",
            "attributes": {
                "label": "Test Wallet"
            }
        }
    }
    response = api_client.post("/api/wallets/", data, format="vnd.api+json")
    assert response.status_code == 201
    assert response.json()["data"]["attributes"]["label"] == "Test Wallet"
    assert response.json()["data"]["attributes"]["balance"] == "0.000000000000000000"


@pytest.mark.django_db
def test_list_wallets(api_client, wallet):
    response = api_client.get("/api/wallets/", format="vnd.api+json")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1


@pytest.mark.django_db
def test_get_wallet(api_client, wallet):
    response = api_client.get(
        f"/api/wallets/{wallet.id}/",
        format="vnd.api+json"
    )
    assert response.status_code == 200
    assert response.json()["data"]["attributes"]["label"] == "Test Wallet"
