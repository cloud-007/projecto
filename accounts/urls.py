from django.urls import path

from .views import (
    SignInView,
    SignOutView,
    RegisterView,
    ProfileView,
)

urlpatterns = [
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
]
