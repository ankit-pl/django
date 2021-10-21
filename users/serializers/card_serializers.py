from rest_framework import serializers
from ..models import Card


class CardSerializer(serializers.ModelSerializer):
    """
    Class to recive stripe card details and return serialized data.
    """

    class Meta:
        model = Card
        fields = ["card_id", "last_transaction_date", "date_created", "user"]

    def add_card(self):
        card = self.save()

        return {
            "message": f"Card created for user '{card.user.email}'",
            "data": {"card": self.validated_data},
        }

    def delete(self):
        card_id = self.instance.card_id
        self.instance.delete()

        return {"message": f"Card with id '{card_id}' deleted."}
