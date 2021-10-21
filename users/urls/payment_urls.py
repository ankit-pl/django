from django.urls import path
from .. import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("me/cards", views.CardsView.as_view(), name="cards"),
]

payment_url_patterns = format_suffix_patterns(urlpatterns)
