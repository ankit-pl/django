from ..models import Wallet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..serializers import (
    BalanceSerializer,
    SuccessSerializer,
    FailureSerializer,
)


class BalanceView(APIView):
    """
    Class to get or add user wallet balance, on successfull request validation
    and return serialized reponse with balance amount or success message,
    respectively.

    In case of validation failure or error, a response with failure message
    will be returned.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        serializer = BalanceSerializer(instance=wallet)
        response_data = SuccessSerializer({"data": serializer.data}).data

        return Response(response_data)

    def put(self, request):
        wallet = Wallet.objects.get(user=request.user)
        serializer = BalanceSerializer(instance=wallet, data=request.data)

        if not serializer.is_valid():
            response_data = FailureSerializer({"data": serializer.errors}).data
        else:
            balance = serializer.add_balance()
            response_data = SuccessSerializer(balance).data

        return Response(response_data)
