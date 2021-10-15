from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils.translation import gettext_lazy

# class CustomeAccountManager(BaseUserManager):
#     def create_user(self, email, username, first_name, password, **other_fields):
#         if not email:
#             raise ValueError(gettext_lazy('You must provide an email address'))

#         email = self.normalize_email(email)

#         user = self.model(email=email, username=username,
#                           first_name=first_name, **other_fields)
#         user.set_password(password)
#         user.save()

#         return user

#     def create_superuser(self, email, username, first_name, password, **other_fields):
#         other_fields.setdefault('is_staff', True)
#         other_fields.setdefault('is_superuser', True)
#         other_fields.setdefault('is_active', True)

#         if other_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must be assigned to is_staff=True')

#         if other_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must be assigned to is_superuser=True')

#         return self.create_user(email, username, first_name, password, **other_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True)
    email = models.CharField(max_length=100, unique=True, null=False)
    username = models.CharField(max_length=100, unique=True, default='')
    password = models.CharField(max_length=255)
    last_login = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    geo_location = models.TextField()
    metadata = models.JSONField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    # def __str__(self):
    #     return self.username
    objects = UserManager()

    class Meta:
        db_table = u'galaxy_user'
