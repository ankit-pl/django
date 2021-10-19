import stripe
from .models import User, Wallet, Card
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    RegisterSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
    ProfileSerializer,
    BalanceSerializer,
    ErrorSerializer,
    SuccessSerializer,
    FailureSerializer,
    CardSerializer,
)
from django.conf import settings


class LoginView(APIView):
    """
    Class to get user logged in on successfull request validation
    and return serialized reponse with auth token.

    In case of validation failure or error, a response with failure message
    will be returned.
    """

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    token = Token.objects.get(user=user).key
                    response_data = SuccessSerializer(
                        data={
                            "message": "User logged-in. \
                                Use auth token to access the API.",
                            "data": {"auth_token": token},
                        }
                    )
                    response_data.is_valid()
                    return Response(response_data.data)
                response_data = FailureSerializer(
                    data={"message": "Please enter the correct password."}
                )
                response_data.is_valid()
                return Response(response_data.data)
            except User.DoesNotExist:
                error = ErrorSerializer(
                    data={"status": 400, "message": "User does not exist."}
                )
                error.is_valid()
                return Response(error.data)
        response_data = FailureSerializer(data={"data": serializer.errors})
        response_data.is_valid()
        return Response(response_data.data)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pass


class RegisterView(APIView):
    """
    Class to get user registered, on successfull request validation
    and return serialized reponse with auth token.

    In case of validation failure or error, a response with failure message
    will be returned.
    """

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user).key
            response_data = SuccessSerializer(
                data={
                    "message": "User registered.\
                        Use auth token to access the API.",
                    "data": {"auth_token": token},
                }
            )
            response_data.is_valid()
            return Response(response_data.data)
        response_data = FailureSerializer(data={"data": serializer.errors})
        response_data.is_valid()
        return Response(response_data.data)


class ChangePasswordView(APIView):
    """
    Class to update user password, on successfull request validation
    and return serialized reponse with success message.

    In case of validation failure or error, a response with failure message
    will be returned.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(instance=request.user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_data = SuccessSerializer(
                data={"message": f"Password for user '{user.email}' updated."}
            )
            response_data.is_valid()
            return Response(response_data.data)
        response_data = FailureSerializer(data={"data": serializer.errors})
        response_data.is_valid()
        return Response(response_data.data)


class ProfileView(APIView):
    """
    Class to get or update user profile, on successfull request validation
    and return serialized reponse with profile details or success
    message, respectively.

    In case of validation failure or error, a response with failure message
    will be returned.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(instance=request.user)
        response_data = SuccessSerializer(data={"data": serializer.data})
        response_data.is_valid()
        return Response(response_data.data)

    def put(self, request):
        serializer = ProfileSerializer(instance=request.user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_data = SuccessSerializer(
                data={"message": f"Profile for user '{user.email}' updated."}
            )
            response_data.is_valid()
            return Response(response_data.data)
        response_data = FailureSerializer(data={"data": serializer.errors})
        response_data.is_valid()
        return Response(response_data.data)

    def util(self, request):
        serializer = ProfileSerializer(instance=request.user)
        response_data = SuccessSerializer(data={"data": serializer.util()})
        response_data.is_valid()
        return Response(response_data.data)


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
        response_data = SuccessSerializer(data={"data": serializer.data})
        response_data.is_valid()
        return Response(response_data.data)

    def put(self, request):
        wallet = Wallet.objects.get(user=request.user)
        serializer = BalanceSerializer(instance=wallet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = SuccessSerializer(
                data={"message": f"Balance for user '{wallet.user}' updated."}
            )
            response_data.is_valid()
            return Response(response_data.data)
        response_data = FailureSerializer(data={"data": serializer.errors})
        response_data.is_valid()
        return Response(response_data.data)


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
        response_data = SuccessSerializer(data={"data": data})
        response_data.is_valid()
        return Response(response_data.data)

    def post(self, request):
        stripe.api_key = settings.STRIPE_API_KEY
        card = stripe.Customer.create_source(
            request.user.customer_id,
            source="tok_mastercard",
        )
        request.data["card_id"] = card.id
        request.data["user"] = request.user.user_id
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = SuccessSerializer(
                data={
                    "message": f"Card created for user '{request.user.email}'",
                    "data": {"card": serializer.data},
                }
            )
            response_data.is_valid()
            return Response(response_data.data)
        response_data = FailureSerializer(data={"data": serializer.errors})
        response_data.is_valid()
        return Response(response_data.data)

    def delete(self, request):
        try:
            card = Card.objects.get(card_id=request.data["card_id"])
            serializer = CardSerializer(instance=card)
            serializer.delete()
            response_data = SuccessSerializer(
                data={
                    "message": f"Card with id '{request.data['card_id']}'\
                        deleted."
                }
            )
            response_data.is_valid()
            return Response(response_data.data)
        except Card.DoesNotExist:
            error = ErrorSerializer(
                data={"status": 400, "message": "Card does not exist."}
            )
            error.is_valid()
            return Response(error.data)
        except Exception:
            error = ErrorSerializer(
                data={"status": 400, "message": "Card id is not provided."}
            )
            error.is_valid()
            return Response(error.data)
