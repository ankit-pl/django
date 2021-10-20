from django.urls import path
from .. import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("me/balance", views.BalanceView.as_view(), name="balance"),
]

wallet_url_patterns = format_suffix_patterns(urlpatterns)
