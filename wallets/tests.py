from django.test import TestCase
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Wallet


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def wallet():
    return Wallet.objects.create(label="Test Wallet", balance=0)


@pytest.mark.django_db
class TestWalletModel:
    def test_wallet_creation(self):
        wallet = Wallet.objects.create(label="Test Wallet")
        assert wallet.label == "Test Wallet"
        assert wallet.balance == 0

    def test_wallet_str(self):
        wallet = Wallet.objects.create(label="Test Wallet")
        assert str(wallet) == "Test Wallet (0)"


@pytest.mark.django_db
class TestWalletAPI:
    def test_create_wallet(self, api_client):
        url = reverse('wallet-list')
        data = {
            "data": {
                "type": "Wallet",
                "attributes": {
                    "label": "Test Wallet"
                }
            }
        }
        response = api_client.post(url, data, format='vnd.api+json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['data']['attributes']['label'] == "Test Wallet"
        assert response.json()['data']['attributes']['balance'] == "0.000000000000000000"

    def test_list_wallets(self, api_client, wallet):
        url = reverse('wallet-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['data']) == 1
        assert response.json()['data'][0]['attributes']['label'] == wallet.label

    def test_get_wallet(self, api_client, wallet):
        url = reverse('wallet-detail', args=[wallet.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['data']['attributes']['label'] == wallet.label

    def test_update_wallet(self, api_client, wallet):
        url = reverse('wallet-detail', args=[wallet.id])
        data = {
            "data": {
                "type": "Wallet",
                "id": str(wallet.id),
                "attributes": {
                    "label": "Updated Wallet"
                }
            }
        }
        response = api_client.patch(url, data, format='vnd.api+json')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['data']['attributes']['label'] == "Updated Wallet"

    def test_delete_wallet(self, api_client, wallet):
        url = reverse('wallet-detail', args=[wallet.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Wallet.objects.filter(id=wallet.id).exists()
