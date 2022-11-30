from django.contrib import admin

from .models import Course, Proposal, Result, Marksheet


@admin.register(Course)
class Course(admin.ModelAdmin):
    list_display = ['title', 'course_id', 'semester']
    search_fields = ['title', 'course_id', 'semester']


@admin.register(Proposal)
class Proposal(admin.ModelAdmin):
    list_display = ['title', 'course', 'assigned_supervisor', 'assigned_by', 'team_lead', 'file']
    search_fields = ['title', 'course__title', 'assigned_supervisor__full_name', 'assigned_by__full_name',
                     'team_lead__full_name']


@admin.register(Result)
class Result(admin.ModelAdmin):
    list_display = ['proposal', 'course', 'student', 'marks']
    search_fields = ['proposal__title', 'course__title', 'student__full_name']


@admin.register(Marksheet)
class Marksheet(admin.ModelAdmin):
    list_display = ['teacher', 'result', 'criteria_1', 'criteria_2', 'supervisor']
    search_fields = ['teacher__full_name', 'result__course__course_id', 'criteria_1', 'criteria_2', 'supervisor']
