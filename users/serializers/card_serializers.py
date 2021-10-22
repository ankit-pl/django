from rest_framework import serializers
from ..models import Card
from django.utils.translation import gettext_lazy as _


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
            "message": _(f"Card created for user '{card.user.email}'"),
            "data": {
                "card_id": card.card_id,
                "last_transaction_date": card.last_transaction_date,
                "date_created": card.date_created,
            },
        }

    def delete(self):
        card_id = self.instance.card_id
        self.instance.delete()

        return {"message": _(f"Card with id '{card_id}' deleted.")}
