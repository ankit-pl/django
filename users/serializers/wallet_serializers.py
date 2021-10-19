from rest_framework import serializers
from ..models import Wallet


class BalanceSerializer(serializers.ModelSerializer):
    """
    Class to recive wallet details and return serialized data.
    """

    class Meta:
        model = Wallet
        fields = ["balance", "currency", "last_transaction_date"]
