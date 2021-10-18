from rest_framework import serializers
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, ChangePasswordSerializer

class LoginView(APIView):
    def post(self, request):
        pass

class LogoutView(APIView):
    def get(self, request):
        pass

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user).key
            return Response(f'User registered. Use "{token}" auth token to access the API.')
        return Response(serializer.errors)

class ChangePasswordView(APIView):
    def post(self, request, email):
        user = User.objects.get(email=email)
        # match existing password
        if True:
            serializer = ChangePasswordSerializer(instance=user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response('failed')
