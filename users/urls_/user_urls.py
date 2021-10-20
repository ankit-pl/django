from django.urls import path
from .. import views

urlpatterns = [
    path("signup", views.RegisterView.as_view(), name="register"),
    path("change-password", views.ChangePasswordView.as_view(), name="change-password"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("profile", views.ProfileView.as_view(), name="profile"),
]
