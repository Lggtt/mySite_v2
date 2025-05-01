# accounts/urls.py

from django.urls import path
from .views import register, activate
from . import views
from django.contrib.auth import views as auth_views
from .views import PrivatePageView

urlpatterns = [
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('private/', PrivatePageView.as_view(), name='private_page'),
]
