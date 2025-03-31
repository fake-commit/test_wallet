from django_filters import rest_framework as django_filters
from rest_framework_json_api.views import ModelViewSet

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionFilter(django_filters.FilterSet):
    min_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')
    wallet = django_filters.UUIDFilter(field_name='wallet')
    txid = django_filters.CharFilter(field_name='txid', lookup_expr='icontains')

    class Meta:
        model = Transaction
        fields = ['min_amount', 'max_amount', 'wallet', 'txid']


class TransactionViewSet(ModelViewSet):
    """
    API endpoint for managing transactions.

    Transactions represent monetary operations within a wallet. Each transaction
    affects the wallet's balance and must have a unique transaction ID (txid).

    list:
    Returns a paginated list of all transactions. Can be filtered by amount range,
    wallet ID, and transaction ID.

    create:
    Creates a new transaction. The amount must be positive, and the wallet must
    have sufficient balance for debit transactions.

    retrieve:
    Returns the details of a specific transaction.

    update:
    Updates are not allowed for transactions to maintain financial integrity.

    partial_update:
    Partial updates are not allowed for transactions.

    delete:
    Deleting transactions is not allowed to maintain financial records.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_class = TransactionFilter
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']
