from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('changepassword/<str:email>', views.ChangePasswordView.as_view(), name='change-password'),
    # path('login', views.login, name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
]
