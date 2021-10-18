import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager
)
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               editable=False)
    email = models.CharField(max_length=100, unique=True, null=False)
    username = models.CharField(max_length=100, unique=True, default="")
    password = models.CharField(max_length=255)
    last_login = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100)
    geo_location = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    metadata = models.JSONField(default=list)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name"]
    objects = UserManager()

    class Meta:
        db_table = u"galaxy_user"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        Wallet.objects.create(user=instance)


class Wallet(models.Model):
    wallet_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                 editable=False)
    balance = models.CharField(max_length=10, default='0')
    currency = models.CharField(max_length=5, default='INR')
    last_transaction_date = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
