import datetime

from django import template

from project_management.models import Course, Proposal

register = template.Library()


@register.filter(name='proposal_3300_count')
def proposal_3300_count(queryset, initials):  # Only one argument.
    return get_course_count(course_code=3300, initials=initials)


@register.filter(name='proposal_4800_count')
def proposal_4800_count(queryset, initials):  # Only one argument.
    return get_course_count(course_code=4800, initials=initials)


@register.filter(name='proposal_4801_count')
def proposal_4801_count(queryset, initials):  # Only one argument.
    return get_course_count(course_code=4801, initials=initials)


def get_course_count(course_code, initials):
    running_courses = Course.objects.filter(
        deadline__range=(
            datetime.datetime.now().date(),
            datetime.date(2500, 1, 1))).order_by(
        'deadline'
    )
    running_courses = running_courses.filter(course_id=course_code)
    print("Running Courses")
    print(running_courses)
    proposals = Proposal.objects.filter(course__in=running_courses, assigned_supervisor__initials=initials)
    cnt = 0
    for proposal in proposals:
        cnt = cnt + proposal.students.count()
    return cnt
