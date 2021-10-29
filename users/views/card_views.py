import stripe
from ..models import Card
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..serializers import (
    ErrorSerializer,
    SuccessSerializer,
    FailureSerializer,
    CardSerializer,
    SuccessSerializerV2,
    FailureSerializerV2,
    CardSerializerV2,
)
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.versioning import AcceptHeaderVersioning
import logging


class CardsView(APIView):
    """
    Class to get or create or delete stripe cards for a user, on
    successfull request validation and return serialized response with
    card info.

    In case of validation failure or error, a response with failure message
    will be returned.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated | HasAPIKey]
    versioning_class = AcceptHeaderVersioning
    logger = logging.getLogger(__name__)

    def get(self, request):
        data = []
        cards = Card.objects.filter(user=request.user)

        if request.version == "1.0":
            for card in cards:
                serializer = CardSerializer(instance=card)
                data.append(serializer.data)

            response_data = SuccessSerializer({"data": data}).data
        else:
            for card in cards:
                serializer = CardSerializerV2(instance=card)
                data.append(serializer.data)

            response_data = SuccessSerializerV2({"data": data}).data

        return Response(response_data)

    def post(self, request):
        stripe.api_key = settings.STRIPE_API_KEY
        card = stripe.Customer.create_source(
            request.user.customer_id,
            source="tok_mastercard",
        )
        request.data["card_id"] = card.id
        request.data["user"] = request.user.user_id

        if request.version == "1.0":
            serializer = CardSerializer(data=request.data)

            if not serializer.is_valid():
                response_data = FailureSerializer({"data": serializer.errors}).data
                self.logger.error(serializer.errors)
            else:
                card = serializer.add_card()
                response_data = SuccessSerializer(card).data
        else:
            serializer = CardSerializerV2(data=request.data)

            if not serializer.is_valid():
                response_data = FailureSerializerV2({"data": serializer.errors}).data
                self.logger.error(serializer.errors)
            else:
                card = serializer.add_card()
                response_data = SuccessSerializerV2(card).data

        return Response(response_data)

    def delete(self, request):
        try:
            card = Card.objects.get(card_id=request.data["card_id"])
            if request.version == "1.0":
                serializer = CardSerializer(instance=card)
                card = serializer.delete()
                response_data = SuccessSerializer(card).data
            else:
                serializer = CardSerializerV2(instance=card)
                card = serializer.delete()
                response_data = SuccessSerializerV2(card).data

            return Response(response_data)
        except Card.DoesNotExist:
            error = ErrorSerializer(
                {"status": 400, "message": _("Card does not exist.")}
            )
            self.logger.error("Card does not exist.")

            return Response(error.data)
        except Exception:
            error = ErrorSerializer(
                {"status": 400, "message": _("Card id is not provided.")}
            )
            self.logger.error("Card id is not provided.")

            return Response(error.data)
