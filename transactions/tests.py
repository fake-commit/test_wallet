from django.test import TestCase
import pytest
from decimal import Decimal
from django.urls import reverse
from django.core.exceptions import ValidationError
from rest_framework import status
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
    return Transaction.objects.create(wallet=wallet, txid="test_tx", amount=1)


@pytest.mark.django_db
class TestTransactionModel:
    def test_transaction_creation(self, wallet):
        transaction = Transaction.objects.create(
            wallet=wallet,
            txid="test_tx",
            amount=1.0
        )
        assert transaction.txid == "test_tx"
        assert float(transaction.amount) == 1.0
        assert float(wallet.balance) == 1.0

    def test_negative_balance_prevention(self, wallet):
        with pytest.raises(ValidationError):
            Transaction.objects.create(
                wallet=wallet,
                txid="test_tx",
                amount=-1.0
            )

    def test_unique_txid(self, wallet):
        Transaction.objects.create(
            wallet=wallet,
            txid="test_tx",
            amount=1.0
        )
        with pytest.raises(Exception):
            Transaction.objects.create(
                wallet=wallet,
                txid="test_tx",
                amount=1.0
            )


@pytest.mark.django_db
class TestTransactionAPI:
    def test_create_transaction(self, api_client, wallet):
        url = reverse('transaction-list')
        data = {
            "data": {
                "type": "Transaction",
                "attributes": {
                    "txid": "test_tx",
                    "amount": "1.00000000"
                },
                "relationships": {
                    "wallet": {
                        "data": {"type": "Wallet", "id": str(wallet.id)}
                    }
                }
            }
        }
        response = api_client.post(url, data, format='vnd.api+json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['data']['attributes']['amount'] == "1.00000000"

    def test_list_transactions(self, api_client, transaction):
        url = reverse('transaction-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['data']) == 1
        assert response.json()['data'][0]['attributes']['txid'] == transaction.txid

    def test_get_transaction(self, api_client, transaction):
        url = reverse('transaction-detail', args=[transaction.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['data']['attributes']['txid'] == transaction.txid

    def test_negative_balance_transaction(self, api_client, wallet):
        url = reverse('transaction-list')
        data = {
            "data": {
                "type": "Transaction",
                "attributes": {
                    "txid": "test_tx",
                    "amount": "-1.00000000"
                },
                "relationships": {
                    "wallet": {
                        "data": {"type": "Wallet", "id": str(wallet.id)}
                    }
                }
            }
        }
        response = api_client.post(url, data, format='vnd.api+json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
