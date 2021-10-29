from django.conf import settings
from rest_framework import serializers
from ..models import User
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class LoginSerializerV2(serializers.ModelSerializer):
    """
    Class to recive user login details and return serialized data.
    """

    class Meta:
        model = User
        fields = ["username", "password"]

    def login(self):
        email = self.validated_data["username"]
        password = self.validated_data["password"]
        user = User.objects.get(email=email)
        if user.check_password(password):
            if not Token.objects.filter(user=user).exists():
                Token.objects.create(user=user)
            response = {
                "message": _("USER LOGGED-IN SUCCESSFULLY."),
                "data": {
                    "USERNAME": user.username,
                    "EMAIL": user.email,
                    "AUTH_TOKEN": user.auth_token.key,
                },
            }
        else:
            response = {
                "message": _("WRONG PASSWORD! PLEASE ENTER THE CORRECT PASSWORD.")
            }
        return response


class LogoutSerializerV2(serializers.ModelSerializer):
    """
    Class to recive current user via auth token and logout it from the system.
    """

    class Meta:
        model = User
        fields = []

    def logout(self):
        if not Token.objects.filter(user=self.instance).exists():
            Token.objects.filter(user=self.instance).delete()

            response = {"message": _("USER LOGGED-OUT SUCCESSFULLY")}
        else:
            response = {"message": _("NO USER IS LOGGED-IN")}
        return response


class RegisterSerializerV2(serializers.ModelSerializer):
    """
    Class to recive user registeration details and return serialized
    data.
    """

    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "first_name", "password", "confirm_password"]

    def save(self):
        user = User(
            email=self.validated_data["email"], username=self.validated_data["username"]
        )
        password = self.validated_data["password"]
        confirm_password = self.validated_data["confirm_password"]
        if password != confirm_password:
            raise serializers.ValidationError(
                {"password": _("PASSWORD AND CONFIRM_PASSWORD DOES NOT MATCH")}
            )
        else:
            user.set_password(password)
            user.save()
        return user

    def register(self):
        user = self.save()

        return {
            "message": _("USER REGISTERED SUCCESSFULLY"),
            "data": {
                "USERNAME": user.username,
                "EMAIL": user.email,
                "AUTH_TOKEN": user.auth_token.key,
            },
        }


class ChangePasswordSerializerV2(serializers.ModelSerializer):
    """
    Class to recive change password details and return serialized
    data.
    """

    class Meta:
        model = User
        fields = ["password"]

    def save(self):
        password = self.validated_data["password"]
        self.instance.set_password(password)
        self.instance.save()
        return self.instance

    def change_password(self):
        user = self.save()

        return {
            "message": _("YOUR PASSWORD HAS BEEN UPDATED, SUCCESSFULLY"),
            "data": {"USERNAME": user.username, "EMAIL": user.email},
        }


class ProfileSerializerV2(serializers.ModelSerializer):
    """
    Class to recive user profile data and return serialized data.
    """

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "image",
            "geo_location",
        ]

    def update_profile(self):
        user = self.save()

        return {
            "message": _("YOUR PROFILE HAS BEEN UPDATED, SUCCESSFULLY"),
            "data": {
                "FIRST_NAME": user.first_name,
                "LAST_NAME": user.last_name,
                "USERNAME": user.username,
                "EMAIL": user.email,
                "IMAGE": user.image,
                "GEO_LOCATION": user.geo_location,
            },
        }

    def util(self):
        base_url = settings.BASE_URL
        media_directory_path = settings.MEDIA_URL + "profile_pics/"
        image = self.instance.image
        return base_url + media_directory_path + image
