import uuid
from django.db import models
from django.db.models import F
from django.core.exceptions import ValidationError
from wallets.models import Wallet


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    txid = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=18, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.wallet.balance + self.amount < 0:
            raise ValidationError("Transaction would result in negative balance")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        # Update wallet balance
        self.wallet.balance += self.amount
        self.wallet.save()

    def __str__(self):
        return f"{self.txid} ({self.amount})"

    class Meta:
        db_table = 'transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['txid']),
            models.Index(fields=['wallet']),
        ]
