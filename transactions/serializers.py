from rest_framework_json_api import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.

    Fields:
        id: The unique identifier of the transaction
        wallet: The ID of the wallet this transaction belongs to
        txid: A unique transaction ID (case-insensitive)
        amount: The transaction amount (positive for deposits, negative for withdrawals)

    Validation:
        - The txid field must be unique across all transactions
        - The amount field must be a valid decimal number
        - For withdrawals (negative amounts), the wallet must have sufficient balance

    The transaction amount affects the wallet's balance:
    - Positive amounts increase the wallet's balance (deposits)
    - Negative amounts decrease the wallet's balance (withdrawals)
    """

    class Meta:
        model = Transaction
        fields = ['id', 'wallet', 'txid', 'amount', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        """
        Validate the transaction data.

        Checks:
        1. For withdrawals (negative amounts), ensure the wallet has sufficient balance
        2. The transaction ID (txid) must be unique
        """
        if data.get("amount", 0) < 0:
            wallet = data.get("wallet")
            if wallet and wallet.balance + data["amount"] < 0:
                raise serializers.ValidationError(
                    "Insufficient funds for this transaction"
                )
        return data
