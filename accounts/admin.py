from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.text import gettext_lazy as _

from .models import User, Student, Teacher, Token


@admin.register(User)
class User(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_verified']
    fieldsets = [
        [None, {'fields': ['username', 'password']}],
        [_('Personal info'), {'fields': ['first_name', 'last_name', 'email']}],
        [_('Permissions'), {
            'fields': ['is_verified', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'],
        }],
        [_('Important dates'), {'fields': ['last_login', 'date_joined']}],
    ]
    date_hierarchy = 'date_joined'


@admin.register(Student)
class Student(admin.ModelAdmin):
    list_display = ['student_id', 'full_name', 'batch', 'section']
    search_fields = ['student_id', 'full_name', 'batch', 'section']


@admin.register(Teacher)
class Teacher(admin.ModelAdmin):
    list_display = ['full_name', 'initials']
    search_fields = ['full_name', 'initials']


@admin.register(Token)
class Token(admin.ModelAdmin):
    pass
