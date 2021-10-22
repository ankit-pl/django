from django.conf import settings
from rest_framework import serializers
from ..models import User
from django.utils.translation import gettext_lazy as _


class LoginSerializer(serializers.ModelSerializer):
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
            response = {
                "message": _("User logged-in. Use auth token to access the API."),
                "data": {"auth_token": user.auth_token.key},
            }
        else:
            response = {"message": _("Please enter the correct password.")}
        return response


class RegisterSerializer(serializers.ModelSerializer):
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
            raise serializers.ValidationError({"password": _("Passwords must match.")})
        else:
            user.set_password(password)
            user.save()
        return user

    def register(self):
        user = self.save()

        return {
            "message": _("User registered. Use auth token to access the API."),
            "data": {"auth_token": user.auth_token.key},
        }


class ChangePasswordSerializer(serializers.ModelSerializer):
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

        return {"message": _(f"Password for user '{user.email}' updated.")}


class ProfileSerializer(serializers.ModelSerializer):
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

        return {"message": _(f"Profile for user '{user.email}' updated.")}

    def util(self):
        base_url = settings.BASE_URL
        media_directory_path = settings.MEDIA_URL + "profile_pics/"
        image = self.instance.image
        return base_url + media_directory_path + image
