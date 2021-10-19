import uuid
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .user import User


class Wallet(models.Model):
    """
    Class to define wallet model.
    """

    currencies = [
        ("INR", "Indian Rupee"),
        ("USD", "United States Dollar"),
        ("CAD", "Canadian Dollar"),
        ("GBP", "Great Britain Pound"),
    ]

    wallet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.IntegerField(default=0)
    currency = models.CharField(max_length=5, choices=currencies, default="INR")
    last_transaction_date = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_wallet(sender, instance=None, created=False, **kwargs):
    if created:
        Wallet.objects.create(user=instance)
