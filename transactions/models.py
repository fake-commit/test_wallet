from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models, transaction
import uuid

from wallets.models import Wallet


class TransactionManager(models.Manager):
    def create(self, **kwargs):
        if not kwargs.get('pk'):  # Only for new transactions
            new_balance = kwargs['wallet'].balance + kwargs['amount']
            if new_balance < 0:
                raise ValidationError("Wallet balance cannot be negative.")
        return super().create(**kwargs)


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    txid = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=36, decimal_places=18)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = TransactionManager()

    def __str__(self):
        return f"{self.txid} - {self.amount}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Only for new transactions
            new_balance = self.wallet.balance + self.amount
            if new_balance < 0:
                raise ValidationError("Wallet balance cannot be negative.")
        with transaction.atomic():
            super().save(*args, **kwargs)
            self.wallet.balance = self.wallet.balance + self.amount
            self.wallet.save()

    class Meta:
        db_table = "transactions"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["txid"]),
            models.Index(fields=["wallet"]),
        ]
