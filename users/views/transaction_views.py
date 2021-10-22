from ..models import Transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..serializers import (
    TransactionSerializer,
    FailureSerializer,
    SuccessSerializerV2,
)
from django.utils.translation import gettext_lazy as _


class TransactionView(APIView):
    """
    Class to get transaction details, on successfull request validation
    and return serialized reponse with transaction data.

    In case of validation failure or error, a response with failure message
    will be returned.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_scope = "transaction"

    def get(self, request, version="v2"):
        if version == "v1":
            response_data = FailureSerializer(
                {"message": _("Feature not available.")}
            ).data
        else:
            data = []
            transactions = Transaction.objects.filter(wallet_id=request.user.wallet)

            for transaction in transactions:
                serializer = TransactionSerializer(instance=transaction)
                data.append(serializer.data)

            response_data = SuccessSerializerV2({"data": data}).data

        return Response(response_data)