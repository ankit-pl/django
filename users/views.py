from .models import User, Wallet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import (RegisterSerializer, ChangePasswordSerializer,
                          LoginSerializer, ProfileSerializer,
                          BalanceSerializer)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    token = Token.objects.get(user=user).key
                    return Response(
                        f'User logged-in.\
                         Use "{token}" auth token to access the API.'
                    )
                return Response("Please enter the correct password.")
            except User.DoesNotExist:
                return Response(
                    f'User with username "{email}" does not exists.'
                )
        return Response(serializer.errors)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pass


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user).key
            return Response(
                f'User registered.\
                             Use "{token}" auth token to access the API.'
            )
        return Response(serializer.errors)


class ChangePasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(instance=request.user,
                                              data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(f'Password for user "{user.email}" updated.')
        return Response(serializer.errors)


class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(instance=request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileSerializer(instance=request.user,
                                       data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(f'Profile for user "{user.email}" updated.')
        return Response(serializer.errors)


class BalanceView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        serializer = BalanceSerializer(instance=wallet)
        return Response(serializer.data)

    def put(self, request):
        wallet = Wallet.objects.get(user=request.user)
        serializer = BalanceSerializer(instance=wallet,
                                       data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(f'Balance for user "{wallet.user}" updated.')
        return Response(serializer.errors)
