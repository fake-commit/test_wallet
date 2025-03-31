from decimal import Decimal
import pytest
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from wallets.models import Wallet
from .models import Transaction


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def wallet():
    return Wallet.objects.create(label="Test Wallet", balance=0)


@pytest.fixture
def transaction(wallet):
    return Transaction.objects.create(
        wallet=wallet,
        txid="test_txid",
        amount=Decimal("1.000000000000000000")
    )


@pytest.mark.django_db
def test_transaction_creation(wallet):
    transaction = Transaction.objects.create(
        wallet=wallet,
        txid="test_txid",
        amount=Decimal("1.000000000000000000")
    )
    assert transaction.amount == Decimal("1.000000000000000000")
    assert transaction.wallet.balance == Decimal("1.000000000000000000")


@pytest.mark.django_db
def test_negative_balance_transaction(wallet):
    with pytest.raises(ValidationError):
        Transaction.objects.create(
            wallet=wallet,
            txid="test_txid_negative",
            amount=Decimal("-1.000000000000000000")
        )


@pytest.mark.django_db
def test_create_transaction(api_client, wallet):
    data = {
        "data": {
            "type": "Transaction",
            "attributes": {
                "txid": "test_txid",
                "amount": "1.000000000000000000"
            },
            "relationships": {
                "wallet": {
                    "data": {"type": "Wallet", "id": str(wallet.id)}
                }
            }
        }
    }
    response = api_client.post("/api/transactions/", data, format="vnd.api+json")
    assert response.status_code == 201
    assert response.json()["data"]["attributes"]["amount"] == "1.000000000000000000"


@pytest.mark.django_db
def test_list_transactions(api_client, transaction):
    response = api_client.get("/api/transactions/", format="vnd.api+json")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1


@pytest.mark.django_db
def test_get_transaction(api_client, transaction):
    response = api_client.get(
        f"/api/transactions/{transaction.id}/",
        format="vnd.api+json"
    )
    assert response.status_code == 200
    assert response.json()["data"]["attributes"]["amount"] == "1.000000000000000000"
