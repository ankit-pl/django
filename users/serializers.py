from rest_framework import serializers
from .models import User, Wallet


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "password",
            "confirm_password"
        ]

    def save(self):
        user = User(
            email=self.validated_data["email"],
            username=self.validated_data["username"]
        )
        password = self.validated_data["password"]
        confirm_password = self.validated_data["confirm_password"]
        if password != confirm_password:
            raise serializers.ValidationError(
                {"password": "Passwords must match."}
            )
        user.set_password(password)
        user.save()
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["password"]

    def save(self):
        password = self.validated_data["password"]
        self.instance.set_password(password)
        self.instance.save()
        return self.instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'email', 'image', 'geo_location']


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['balance', 'currency', 'last_transaction_date']
