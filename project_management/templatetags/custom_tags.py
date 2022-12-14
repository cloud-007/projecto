import datetime

from django import template

from project_management.models import Course, Proposal

register = template.Library()


@register.filter(name='proposal_3300_count')
def proposal_3300_count(queryset, initials):  # Only one argument.
    running_courses = Course.objects.filter(
        deadline__range=(
            datetime.datetime.now().date(),
            datetime.date(2500, 1, 1))).order_by(
        'deadline'
    )
    running_courses = running_courses.filter(course_id=3300)
    print("Running Courses")
    print(running_courses)
    proposals = Proposal.objects.filter(course__in=running_courses, assigned_supervisor__initials=initials)
    cnt = 0
    for proposal in proposals:
        cnt = cnt + proposal.students.count()
    return cnt


@register.filter(name='proposal_4800_count')
def proposal_4800_count(queryset, initials):  # Only one argument.
    running_courses = Course.objects.filter(
        deadline__range=(
            datetime.datetime.now().date(),
            datetime.date(2500, 1, 1))).order_by(
        'deadline'
    )
    running_courses = running_courses.filter(course_id=4800)
    print("Running Courses")
    print(running_courses)
    proposals = Proposal.objects.filter(course__in=running_courses, assigned_supervisor__initials=initials)
    cnt = 0
    for proposal in proposals:
        cnt = cnt + proposal.students.count()
    return cnt


@register.filter(name='proposal_4801_count')
def proposal_4801_count(queryset, initials):  # Only one argument.
    running_courses = Course.objects.filter(
        deadline__range=(
            datetime.datetime.now().date(),
            datetime.date(2500, 1, 1))).order_by(
        'deadline'
    )
    running_courses = running_courses.filter(course_id=4801)
    print("Running Courses")
    print(running_courses)
    proposals = Proposal.objects.filter(course__in=running_courses, assigned_supervisor__initials=initials)
    cnt = 0
    for proposal in proposals:
        cnt = cnt + proposal.students.count()
    return cnt
