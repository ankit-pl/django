from rest_framework import serializers
from ..models import WalletInformation, Transaction
from django.utils.translation import gettext_lazy as _


class BalanceSerializerV2(serializers.ModelSerializer):
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
            "TRANSACTION_ID": transaction.transaction_id,
            "TYPE": transaction.type,
            "AMOUNT": transaction.amount,
            "TRANSACTION_DETAILS": transaction.transaction_details,
            "STATUS": transaction.status,
            "DATE_CREATED": transaction.date_created,
            "WALLET": transaction.wallet.wallet_id,
        }

        return {
            "message": _(
                f"{transaction.amount} {wallet.currency} HAS BEEN ADDED TO YOUR WALLET BALANCE"
            ),
            "data": data,
        }
