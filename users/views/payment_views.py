import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..serializers import (
    FailureSerializer,
    FailureSerializerV2,
    SuccessSerializerV2,
)
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.versioning import AcceptHeaderVersioning
import logging


class PaymentView(APIView):
    """
    Class to create stripe payments for a user, on successfull request
    validation and return serialized response with payment info.

    In case of validation failure or error, a response with failure message
    will be returned.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated | HasAPIKey]
    versioning_class = AcceptHeaderVersioning
    logger = logging.getLogger(__name__)

    def post(self, request):
        if request.version == "1.0":
            response_data = FailureSerializer(
                {"message": _("Feature not available.")}
            ).data
            self.logger.error("Feature not available.")
        else:
            stripe.api_key = settings.STRIPE_API_KEY
            if not request.data.get("customer"):
                response_data = FailureSerializerV2(
                    {
                        "message": "CUSTOMER PARAMETER MISSING. PLEASE INCLUDE `CUSTOMER` PARAMETER IN REQUEST BODY."
                    }
                ).data
                self.logger.error("CUSTOMER PARAMETER MISSING. PLEASE INCLUDE `CUSTOMER` PARAMETER IN REQUEST BODY.")
            else:
                payment = stripe.PaymentIntent.create(**request.data)
                response_data = SuccessSerializerV2({"data": payment}).data

        return Response(response_data)
