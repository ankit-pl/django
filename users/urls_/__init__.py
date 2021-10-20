from . import wallet_urls
from . import payment_urls
from . import user_urls
from django.urls import path, include

urlpatterns = [
    path("me/", include([wallet_urls, payment_urls, user_urls])),
]
