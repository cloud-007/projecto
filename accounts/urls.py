from django.urls import path

from .views import HomeView, SignInView, SignOutView, RegisterView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]
