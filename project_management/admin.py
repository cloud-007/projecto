from django.contrib import admin

from .models import Course, Proposal, Result, Marksheet

# Register your models here.
myModels = [Course, Proposal, Result, Marksheet]  # iterable list
admin.site.register(myModels)
