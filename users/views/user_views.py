from ..models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from ..serializers import (
    RegisterSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
    ProfileSerializer,
    ErrorSerializer,
    SuccessSerializer,
    FailureSerializer,
)


class LoginView(APIView):
    """
    Class to get user logged in on successfull request validation
    and return serialized reponse with auth token.

    In case of validation failure or error, a response with failure message
    will be returned.
    """

    permission_classes = [HasAPIKey]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            response_data = FailureSerializer({"data": serializer.errors}).data
        else:
            try:
                user = serializer.login()
                if user.get("data"):
                    response_data = SuccessSerializer(user).data
                else:
                    response_data = FailureSerializer(user).data
            except User.DoesNotExist:
                error = ErrorSerializer(
                    {"status": 400, "message": "User does not exist."}
                )
                return Response(error.data)

        return Response(response_data)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated | HasAPIKey ]

    def get(self, request):
        pass


class RegisterView(APIView):
    """
    Class to get user registered, on successfull request validation
    and return serialized reponse with auth token.

    In case of validation failure or error, a response with failure message
    will be returned.
    """
    permission_classes = [HasAPIKey]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            response_data = FailureSerializer({"data": serializer.errors}).data
        else:
            user = serializer.register()
            response_data = SuccessSerializer(user).data

        return Response(response_data)


class ChangePasswordView(APIView):
    """
    Class to update user password, on successfull request validation
    and return serialized reponse with success message.

    In case of validation failure or error, a response with failure message
    will be returned.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated | HasAPIKey]

    def post(self, request):
        serializer = ChangePasswordSerializer(instance=request.user, data=request.data)

        if not serializer.is_valid():
            response_data = FailureSerializer({"data": serializer.errors}).data
        else:
            user = serializer.change_password()
            response_data = SuccessSerializer(user).data

        return Response(response_data)


class ProfileView(APIView):
    """
    Class to get or update user profile, on successfull request validation
    and return serialized reponse with profile details or success
    message, respectively.

    In case of validation failure or error, a response with failure message
    will be returned.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated | HasAPIKey]

    def get(self, request):
        serializer = ProfileSerializer(instance=request.user)
        response_data = SuccessSerializer({"data": serializer.data}).data

        return Response(response_data)

    def put(self, request):
        serializer = ProfileSerializer(instance=request.user, data=request.data)

        if not serializer.is_valid():
            response_data = FailureSerializer({"data": serializer.errors}).data
        else:
            user = serializer.update_profile()
            response_data = SuccessSerializer(user).data

        return Response(response_data)

    def util(self, request):
        serializer = ProfileSerializer(instance=request.user)
        response_data = SuccessSerializer({"data": serializer.util()}).data

        return Response(response_data)
