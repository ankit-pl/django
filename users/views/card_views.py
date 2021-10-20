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
)
from django.conf import settings


class CardsView(APIView):
    """
    Class to get or create or delete stripe cards for a user, on
    successfull request validation and return serialized response with
    card info.

    In case of validation failure or error, a response with failure message
    will be returned.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = []
        cards = Card.objects.filter(user=request.user)

        for card in cards:
            serializer = CardSerializer(instance=card)
            data.append(serializer.data)

        response_data = SuccessSerializer({"data": data}).data

        return Response(response_data)

    def post(self, request):
        stripe.api_key = settings.STRIPE_API_KEY
        card = stripe.Customer.create_source(
            request.user.customer_id,
            source="tok_mastercard",
        )
        request.data["card_id"] = card.id
        request.data["user"] = request.user.user_id
        serializer = CardSerializer(data=request.data)

        if not serializer.is_valid():
            response_data = FailureSerializer({"data": serializer.errors}).data
        else:
            card = serializer.add_card()
            response_data = SuccessSerializer(card).data

        return Response(response_data)

    def delete(self, request):
        try:
            card = Card.objects.get(card_id=request.data["card_id"])
            serializer = CardSerializer(instance=card)
            card = serializer.delete()
            response_data = SuccessSerializer(card).data

            return Response(response_data)
        except Card.DoesNotExist:
            error = ErrorSerializer({"status": 400, "message": "Card does not exist."})

            return Response(error.data)
        except Exception:
            error = ErrorSerializer(
                {"status": 400, "message": "Card id is not provided."}
            )

            return Response(error.data)
