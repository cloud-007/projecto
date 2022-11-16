from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    pass


class Student(models.Model):
    full_name = models.CharField(verbose_name=_('Full Name'), max_length=128)
    student_id = models.CharField(verbose_name=_('Student Id'), max_length=30)
    batch = models.IntegerField(verbose_name=_('Batch'))
    section = models.CharField(verbose_name=_('Section'), max_length=10, null=True, blank=True)
    user = models.OneToOneField(
        verbose_name=_('User'),
        to='accounts.User',
        related_name='student',
        on_delete=models.PROTECT
    )
    profile_image = models.ImageField(verbose_name=_('Profile'), upload_to='profile/', null=True, blank=True)

    def __str__(self):
        return self.full_name


class Teacher(models.Model):
    full_name = models.CharField(verbose_name=_('Full Name'), max_length=128)
    initials = models.CharField(verbose_name=_('Initials'), max_length=20)
    user = models.OneToOneField(
        verbose_name=_('User'),
        to='accounts.User',
        related_name='teacher',
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.full_name

    # full_name = models.CharField(verbose_name=_('Full Name'), max_length=128)
