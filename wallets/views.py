from django.shortcuts import render
from rest_framework_json_api.views import ModelViewSet
from django_filters import rest_framework as filters
from .models import Wallet
from .serializers import WalletSerializer


class WalletFilter(filters.FilterSet):
    min_balance = filters.NumberFilter(field_name="balance", lookup_expr='gte')
    max_balance = filters.NumberFilter(field_name="balance", lookup_expr='lte')
    label = filters.CharFilter(field_name="label", lookup_expr='icontains')

    class Meta:
        model = Wallet
        fields = ['min_balance', 'max_balance', 'label']


class WalletViewSet(ModelViewSet):
    """
    API endpoint for managing wallets.
    
    Wallets represent user accounts that can hold a balance and have associated transactions.
    The balance field is read-only and is automatically managed through transactions.
    
    list:
        Return a list of all wallets.
        Can be filtered by:
        - min_balance: Filter wallets with balance greater than or equal to this value
        - max_balance: Filter wallets with balance less than or equal to this value
        - label: Search wallets by label (case-insensitive)
        
        Can be ordered by:
        - balance: Order by wallet balance
        - label: Order by wallet label
        
    create:
        Create a new wallet.
        Required fields:
        - label: A descriptive name for the wallet
        
    retrieve:
        Return details of a specific wallet.
        
    update:
        Update all fields of a specific wallet.
        The balance field cannot be modified directly.
        
    partial_update:
        Update one or more fields of a specific wallet.
        The balance field cannot be modified directly.
        
    delete:
        Delete a specific wallet.
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filterset_class = WalletFilter
    ordering_fields = ['balance', 'label']
    ordering = ['label']
