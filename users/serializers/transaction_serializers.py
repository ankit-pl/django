from rest_framework import serializers
from ..models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """
    Class to handle transaction related details and return serialized data.
    """

    class Meta:
        model = Transaction
        fields = [
            "transaction_id",
            "type",
            "amount",
            "transaction_details",
            "status",
            "date_created",
            "wallet_id",
        ]
