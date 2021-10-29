from django.urls import path
from .. import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("me/cards", views.CardsView.as_view(), name="cards"),
    path("me/transaction", views.TransactionView.as_view(), name="transactions"),
    path("me/payment", views.PaymentView.as_view(), name="payments"),
]

payment_url_patterns = format_suffix_patterns(urlpatterns)
