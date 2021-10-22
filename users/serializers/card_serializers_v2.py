from rest_framework import serializers
from ..models import Card
from django.utils.translation import gettext_lazy as _


class CardSerializerV2(serializers.ModelSerializer):
    """
    Class to recive stripe card details and return serialized data.
    """

    class Meta:
        model = Card
        fields = ["card_id", "last_transaction_date", "date_created", "user"]

    def add_card(self):
        card = self.save()

        return {
            "message": _("NEW CARD HAS BEEN ADDED"),
            "data": {
                "CARD_ID": card.card_id,
                "LAST_TRANSACTION_DATE": card.last_transaction_date,
                "DATE_CREATED": card.date_created,
                "USER": card.user.email,
            },
        }

    def delete(self):
        card = self.instance
        self.instance.delete()

        return {
            "message": _("YOUR CARD HAS BEEN DELETED, SUCCESSFULLY"),
            "data": {
                "CARD_ID": card.card_id,
                "LAST_TRANSACTION_DATE": card.last_transaction_date,
                "DATE_CREATED": card.date_created,
                "USER": card.user.email,
            },
        }
