from rest_framework_json_api import serializers
from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    """
    Serializer for the Wallet model.
    
    Fields:
        id: The unique identifier of the wallet
        label: A human-readable label for the wallet
        balance: The current balance of the wallet (read-only)
        
    The balance field is automatically calculated based on the sum of all transactions
    associated with this wallet. It cannot be directly modified through the API.
    """
    class Meta:
        model = Wallet
        fields = ['id', 'label', 'balance']
        read_only_fields = ['balance'] 