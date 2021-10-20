from rest_framework import serializers
from ..models import Wallet, Transaction


class BalanceSerializer(serializers.ModelSerializer):
    """
    Class to recive wallet details and return serialized data.
    """

    class Meta:
        model = Wallet
        fields = ["balance", "currency", "last_transaction_date"]

    def add_balance(self):
        wallet = self.save()
        Transaction.objects.create(amount=wallet.balance, wallet=wallet)

        return {"message": f"Balance for user '{wallet.user}' updated."}
