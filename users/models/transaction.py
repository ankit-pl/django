import uuid
from django.db import models
from .. import TransactionType
from . import WalletInformation


class Transaction(models.Model):
    transaction_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    type = models.CharField(
        max_length=10,
        choices=[(type, type.value) for type in TransactionType],
        default="cash_in",
    )
    amount = models.IntegerField(default=0)
    transaction_details = models.JSONField(default=list)
    status = models.CharField(max_length=50, default="Unknown")
    date_created = models.DateTimeField(auto_now_add=True)
    wallet = models.ForeignKey(
        WalletInformation, related_name="transactions", on_delete=models.CASCADE
    )
