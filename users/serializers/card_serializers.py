from rest_framework import serializers
from ..models import Card


class CardSerializer(serializers.ModelSerializer):
    """
    Class to recive stripe card details and return serialized data.
    """

    class Meta:
        model = Card
        fields = ["card_id", "last_transaction_date", "date_created", "user"]

    def delete(self):
        self.instance.delete()
        return True
