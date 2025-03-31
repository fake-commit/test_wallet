import uuid
from django.db import models
from django.core.validators import MinValueValidator


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=255)
    balance = models.DecimalField(
        max_digits=36,
        decimal_places=18,
        default=0,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        db_table = 'wallets'
        ordering = ['label']

    def __str__(self):
        return f"{self.label} ({self.balance})"
