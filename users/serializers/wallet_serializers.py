from rest_framework import serializers
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
        self.instance.balance += self.validated_data['balance']
        self.instance.save()
        wallet = self.instance
        Transaction.objects.create(amount=self.validated_data['balance'], wallet=wallet)

        return {"message": _(f"Balance for user '{wallet.user}' added.")}
