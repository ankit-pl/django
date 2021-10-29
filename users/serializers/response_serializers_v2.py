from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class SuccessSerializerV2(serializers.Serializer):
    """
    Class to recive success response and return serialized reponse object.
    """

    status = serializers.IntegerField(default=200)
    message = serializers.CharField(
        max_length=100, default=_("REQUEST EXECUTED SUCCESSFULLY")
    )
    data = serializers.JSONField(default=list)


class FailureSerializerV2(serializers.Serializer):
    """
    Class to recive failure response and return serialized reponse object.
    """

    status = serializers.IntegerField(default=400)
    message = serializers.CharField(
        max_length=100, default=_("REQUEST FAILED! CHECK YOUR INPUTS")
    )
    data = serializers.JSONField(default=list)


class ErrorSerializerV2(serializers.Serializer):
    """
    Class to recive error response and return serialized reponse object.
    """

    status = serializers.IntegerField(default=500)
    message = serializers.CharField(
        max_length=100, default=_("SOMETHING WENT WRONG! PLEASE TRY AGAIN")
    )
    data = serializers.JSONField(default=list)
