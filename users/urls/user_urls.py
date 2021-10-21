from django.urls import path
from .. import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("signup", views.RegisterView.as_view(), name="signup"),
    path("change-password", views.ChangePasswordView.as_view(),
         name="change-password"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("me/profile", views.ProfileView.as_view(), name="profile"),
]

user_url_patterns = format_suffix_patterns(urlpatterns)
