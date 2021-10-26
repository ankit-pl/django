from ..models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..serializers import (
    RegisterSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
    ProfileSerializer,
    ErrorSerializer,
    SuccessSerializer,
    FailureSerializer,
    RegisterSerializerV2,
    ChangePasswordSerializerV2,
    LoginSerializerV2,
    ProfileSerializerV2,
    ErrorSerializerV2,
    SuccessSerializerV2,
    FailureSerializerV2,
    LogoutSerializer,
    LogoutSerializerV2,
)
from django.utils.translation import gettext_lazy as _
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.versioning import AcceptHeaderVersioning


class LoginView(APIView):
    """
    Class to get user logged in on successfull request validation
    and return serialized reponse with auth token.

    In case of validation failure or error, a response with failure message
    will be returned.
    """

    permission_classes = [HasAPIKey]
    versioning_class = AcceptHeaderVersioning

    def post(self, request):
        if request.version == "1.0":
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
                        {"status": 400, "message": _("User does not exist")}
                    )
                    return Response(error.data)
        else:
            serializer = LoginSerializerV2(data=request.data)
            if not serializer.is_valid():
                response_data = FailureSerializerV2({"data": serializer.errors}).data
            else:
                try:
                    user = serializer.login()
                    if user.get("data"):
                        response_data = SuccessSerializerV2(user).data
                    else:
                        response_data = FailureSerializerV2(user).data
                except User.DoesNotExist:
                    error = ErrorSerializerV2(
                        {"status": 400, "message": _("User does not exist")}
                    )
                    return Response(error.data)

        return Response(response_data)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated | HasAPIKey]
    versioning_class = AcceptHeaderVersioning

    def get(self, request):
        if request.version == "1.0":
            serializer = LogoutSerializer(instance=request.user)
            user = serializer.logout()
            response_data = SuccessSerializer(user).data
        else:
            serializer = LogoutSerializerV2(instance=request.user)
            user = serializer.logout()
            response_data = SuccessSerializerV2(user).data

        return Response(response_data)


class RegisterView(APIView):
    """
    Class to get user registered, on successfull request validation
    and return serialized reponse with auth token.

    In case of validation failure or error, a response with failure message
    will be returned.
    """

    throttle_scope = "signup"
    permission_classes = [HasAPIKey]
    versioning_class = AcceptHeaderVersioning

    def post(self, request):
        if request.version == "1.0":
            serializer = RegisterSerializer(data=request.data)

            if not serializer.is_valid():
                response_data = FailureSerializer({"data": serializer.errors}).data
            else:
                user = serializer.register()
                response_data = SuccessSerializer(user).data
        else:
            serializer = RegisterSerializerV2(data=request.data)

            if not serializer.is_valid():
                response_data = FailureSerializerV2({"data": serializer.errors}).data
            else:
                user = serializer.register()
                response_data = SuccessSerializerV2(user).data

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
    versioning_class = AcceptHeaderVersioning

    def post(self, request):
        if request.version == "1.0":
            serializer = ChangePasswordSerializer(
                instance=request.user, data=request.data
            )

            if not serializer.is_valid():
                response_data = FailureSerializer({"data": serializer.errors}).data
            else:
                user = serializer.change_password()
                response_data = SuccessSerializer(user).data
        else:
            serializer = ChangePasswordSerializerV2(
                instance=request.user, data=request.data
            )

            if not serializer.is_valid():
                response_data = FailureSerializerV2({"data": serializer.errors}).data
            else:
                user = serializer.change_password()
                response_data = SuccessSerializerV2(user).data

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
    versioning_class = AcceptHeaderVersioning

    def get(self, request):
        if request.version == "1.0":
            serializer = ProfileSerializer(instance=request.user)
            response_data = SuccessSerializer({"data": serializer.data}).data
        else:
            serializer = ProfileSerializerV2(instance=request.user)
            response_data = SuccessSerializerV2({"data": serializer.data}).data

        return Response(response_data)

    def put(self, request):
        if request.version == "1.0":
            serializer = ProfileSerializer(instance=request.user, data=request.data)

            if not serializer.is_valid():
                response_data = FailureSerializer({"data": serializer.errors}).data
            else:
                user = serializer.update_profile()
                response_data = SuccessSerializer(user).data
        else:
            serializer = ProfileSerializerV2(instance=request.user, data=request.data)

            if not serializer.is_valid():
                response_data = FailureSerializerV2({"data": serializer.errors}).data
            else:
                user = serializer.update_profile()
                response_data = SuccessSerializerV2(user).data

        return Response(response_data)

    def util(self, request):
        if request.version == "1.0":
            serializer = ProfileSerializer(instance=request.user)
            response_data = SuccessSerializer({"data": serializer.util()}).data
        else:
            serializer = ProfileSerializerV2(instance=request.user)
            response_data = SuccessSerializerV2({"data": serializer.util()}).data

        return Response(response_data)
