from django.urls import path

from .views import (
    SignInView,
    SignOutView,
    RegisterView,
    ProfileView,
    TeacherManagementView,
    AddTeacherView
)

urlpatterns = [
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('teacher-management/', TeacherManagementView.as_view(), name='teacher-management'),
    path('teacher-management/add-teacher/', AddTeacherView.as_view(), name='add-teacher'),
]
