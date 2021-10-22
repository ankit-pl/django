from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class SuccessSerializer(serializers.Serializer):
    """
    Class to recive success response and return serialized reponse object.
    """

    status = serializers.IntegerField(default=200)
    message = serializers.CharField(max_length=100, default=_("Success"))
    data = serializers.JSONField(default=list)


class FailureSerializer(serializers.Serializer):
    """
    Class to recive failure response and return serialized reponse object.
    """

    status = serializers.IntegerField(default=400)
    message = serializers.CharField(max_length=100, default=_("Bad Request"))
    data = serializers.JSONField(default=list)


class ErrorSerializer(serializers.Serializer):
    """
    Class to recive error response and return serialized reponse object.
    """

    status = serializers.IntegerField(default=500)
    message = serializers.CharField(max_length=100, default=_("Internal Server Error"))
    data = serializers.JSONField(default=list)
