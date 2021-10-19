from django.db import models
from .user import User


class Card(models.Model):
    """
    Class to define cards model.
    """

    card_id = models.TextField(null=False, unique=True)
    last_transaction_date = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
