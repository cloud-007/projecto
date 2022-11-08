from django.contrib import admin

from .models import User, Student, Teacher

myModels = [User, Student, Teacher]  # iterable list
admin.site.register(myModels)
