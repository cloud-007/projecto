from django.contrib.auth import views as auth_view
from django.urls import path

from .views import (
    SignInView,
    SignOutView,
    RegisterView,
    ProfileView,
    TeacherManagementView,
    AddTeacherView, AccountConfirmationView,
)

urlpatterns = [
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('teacher-management/', TeacherManagementView.as_view(), name='teacher-management'),
    path('teacher-management/add-teacher/', AddTeacherView.as_view(), name='add-teacher'),
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name='password-reset'),
    path('password-reset/done/',
         auth_view.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_view.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_view.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    path('register/account-confirmation/<uidb64>/<token>/',
         AccountConfirmationView.as_view(),
         name='account-confirmation'),
]
