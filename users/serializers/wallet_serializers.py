from rest_framework import serializers
from django.core import serializers as core_ser
from ..models import WalletInformation, Transaction
from django.utils.translation import gettext_lazy as _


class BalanceSerializer(serializers.ModelSerializer):
    """
    Class to recive wallet details and return serialized data.
    """

    class Meta:
        model = WalletInformation
        fields = ["balance", "currency", "last_transaction_date"]

    def add_balance(self):
        self.instance.balance += self.validated_data["balance"]
        self.instance.save()
        wallet = self.instance
        transaction = Transaction.objects.create(
            amount=self.validated_data["balance"], wallet=wallet
        )
        data = {
            "transaction_id": transaction.transaction_id,
            "type": transaction.type,
            "amount": transaction.amount,
            "transaction_details": transaction.transaction_details,
            "status": transaction.status,
            "date_created": transaction.date_created,
            "wallet": transaction.wallet.wallet_id,
        }

        return {"message": _(f"Balance for user '{wallet.user}' added."), "data": data}
