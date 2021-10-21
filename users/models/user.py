import uuid
import stripe
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractBaseUser, PermissionsMixin):
    """
    Class to define custom user model.
    """

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=100, unique=True, null=False)
    username = models.CharField(max_length=100, unique=True, default="")
    password = models.CharField(max_length=255)
    last_login = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100)
    geo_location = models.TextField()
    image = models.CharField(max_length=255, default="default.jpg")
    metadata = models.JSONField(default=list)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    customer_id = models.TextField(default="")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name"]
    objects = UserManager()

    class Meta:
        db_table = u"galaxy_user"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_stripe_customer(sender, instance=None, created=False, **kwargs):
    if created:
        stripe.api_key = settings.STRIPE_API_KEY
        customer = stripe.Customer.create()
        instance.customer_id = customer.id
        instance.save()
