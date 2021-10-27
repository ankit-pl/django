from ..models import WalletInformation
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..serializers import (
    BalanceSerializer,
    SuccessSerializer,
    FailureSerializer,
    BalanceSerializerV2,
    SuccessSerializerV2,
    FailureSerializerV2,
)
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.versioning import AcceptHeaderVersioning
import logging


class BalanceView(APIView):
    """
    Class to get or add user wallet balance, on successfull request validation
    and return serialized reponse with balance amount or success message,
    respectively.

    In case of validation failure or error, a response with failure message
    will be returned.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated | HasAPIKey]
    throttle_scope = "transaction"
    versioning_class = AcceptHeaderVersioning
    logger = logging.getLogger(__name__)

    def get(self, request):
        wallet = WalletInformation.objects.get(user=request.user)

        if request.version == "1.0":
            serializer = BalanceSerializer(instance=wallet)
            response_data = SuccessSerializer({"data": serializer.data}).data
        else:
            serializer = BalanceSerializerV2(instance=wallet)
            response_data = SuccessSerializerV2({"data": serializer.data}).data

        self.logger.info("test error")
        return Response(response_data)

    def put(self, request):
        wallet = WalletInformation.objects.get(user=request.user)

        if request.version == "1.0":
            serializer = BalanceSerializer(instance=wallet, data=request.data)

            if not serializer.is_valid():
                response_data = FailureSerializer({"data": serializer.errors}).data
            else:
                balance = serializer.add_balance()
                response_data = SuccessSerializer(balance).data
        else:
            serializer = BalanceSerializerV2(instance=wallet, data=request.data)

            if not serializer.is_valid():
                response_data = FailureSerializerV2({"data": serializer.errors}).data
            else:
                balance = serializer.add_balance()
                response_data = SuccessSerializerV2(balance).data

        return Response(response_data)
