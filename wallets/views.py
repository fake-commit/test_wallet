from django_filters import rest_framework as django_filters
from rest_framework_json_api.views import ModelViewSet

from .models import Wallet
from .serializers import WalletSerializer


class WalletFilter(django_filters.FilterSet):
    min_balance = django_filters.NumberFilter(field_name='balance', lookup_expr='gte')
    max_balance = django_filters.NumberFilter(field_name='balance', lookup_expr='lte')
    label = django_filters.CharFilter(field_name='label', lookup_expr='icontains')

    class Meta:
        model = Wallet
        fields = ['min_balance', 'max_balance', 'label']


class WalletViewSet(ModelViewSet):
    """
    API endpoint for managing wallets.

    Wallets represent accounts that can hold and transfer funds. Each wallet
    maintains a balance and is identified by a unique label.

    list:
    Returns a paginated list of all wallets. Can be filtered by balance range
    and label.

    create:
    Creates a new wallet with the specified label. Initial balance is set to 0.

    retrieve:
    Returns the details of a specific wallet.

    update:
    Updates the label of a specific wallet. Balance cannot be directly modified.

    partial_update:
    Updates the label of a specific wallet. Balance cannot be directly modified.

    delete:
    Deletes a specific wallet if it has a zero balance.
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filterset_class = WalletFilter
    ordering_fields = ['created_at', 'balance', 'label']
    ordering = ['-created_at']
