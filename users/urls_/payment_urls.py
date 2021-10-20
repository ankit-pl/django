from django.urls import path
from .. import views

urlpatterns = [
    path("cards", views.CardsView.as_view(), name="cards"),
]
