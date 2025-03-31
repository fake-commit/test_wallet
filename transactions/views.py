from django.shortcuts import render
from rest_framework_json_api.views import ModelViewSet
from django_filters import rest_framework as filters
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionFilter(filters.FilterSet):
    min_amount = filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name="amount", lookup_expr='lte')
    wallet = filters.NumberFilter(field_name="wallet__id")
    txid = filters.CharFilter(field_name="txid", lookup_expr='icontains')

    class Meta:
        model = Transaction
        fields = ['min_amount', 'max_amount', 'wallet', 'txid']


class TransactionViewSet(ModelViewSet):
    """
    API endpoint for managing transactions.
    
    Transactions represent money movements between wallets.
    Each transaction has a unique transaction ID (txid) and affects the balance of its associated wallet.
    Negative transactions (withdrawals) are only allowed if the wallet has sufficient balance.
    
    list:
        Return a list of all transactions.
        Can be filtered by:
        - min_amount: Filter transactions with amount greater than or equal to this value
        - max_amount: Filter transactions with amount less than or equal to this value
        - wallet: Filter transactions by wallet ID
        - txid: Search transactions by transaction ID (case-insensitive)
        
        Can be ordered by:
        - amount: Order by transaction amount
        - created_at: Order by transaction creation date
        
    create:
        Create a new transaction.
        Required fields:
        - wallet: The ID of the wallet this transaction belongs to
        - txid: A unique transaction ID
        - amount: The transaction amount (positive for deposits, negative for withdrawals)
        
        Note: Withdrawals (negative amounts) will fail if the wallet has insufficient balance.
        
    retrieve:
        Return details of a specific transaction.
        
    update:
        Update all fields of a specific transaction.
        Note: Updating transactions may affect wallet balances.
        
    partial_update:
        Update one or more fields of a specific transaction.
        Note: Updating transactions may affect wallet balances.
        
    delete:
        Delete a specific transaction.
        Note: Deleting transactions may affect wallet balances.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_class = TransactionFilter
    ordering_fields = ['amount', 'created_at']
    ordering = ['-id']
