import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from accounts.models import Teacher
from project_management.models import Course, Proposal


class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        running_courses = Course.objects.filter(
            deadline__range=(datetime.datetime.now().date(), datetime.date(2500, 1, 1))).order_by('deadline')
        archived_courses = Course.objects.filter(
            deadline__range=(datetime.date(2000, 1, 1), datetime.datetime.now().date())).order_by('deadline')

        return render(request, self.template_name,
                      {'courses': running_courses, 'archived': archived_courses})


def post(self, request, *args, **kwargs):
    return render(request, self.template_name, {})


class ProjectDetailsView(LoginRequiredMixin, View):
    template_name = 'project_management/project_details.html'

    context = {
        'course': Course(),
        'proposals': Proposal(),
        'filter_by': 'all',
        'teachers': Teacher.objects.all()
    }

    def get(self, request, *args, **kwargs):
        print(args)
        print(kwargs)
        course_id = kwargs.get('id')
        print(course_id)
        course = Course.objects.get(id=course_id)
        filter_by = kwargs.get('filter_by')

        if filter_by == 'all':
            proposals = course.proposal_set.all()
        elif filter_by == 'assigned':
            proposals = course.proposal_set.filter(assigned_supervisor__isnull=False)
        else:
            proposals = course.proposal_set.filter(assigned_supervisor__isnull=True)

        print(proposals)

        print(course)
        self.context = {
            'course': course,
            'proposals': proposals,
            'filter_by': filter_by,
            'teachers': Teacher.objects.all()
        }

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        return render(request, self.template_name, self.context)


class CreateNewCourse(LoginRequiredMixin, View):
    template_name = 'project_management/create_new_course.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        course = Course()
        course.course_id = request.POST.get("course_code")
        course.title = request.POST.get("course_title")
        course.semester = request.POST.get("semester")
        course.deadline = request.POST.get("deadline")

        context = {
            'course': course
        }

        if Course.objects.filter(course_id=course.course_id, semester=course.semester).first():
            messages.warning(request, "This course for this semester already exists")
            return render(request, self.template_name, context=context)

        course.save()
        messages.success(request, course.title + " has been added successfully")
        return redirect('home')


class UpdateCourseView(LoginRequiredMixin, View):
    template_name = 'project_management/update_course_view.html'

    context = {
        'course': ''
    }

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('id')
        course = Course.objects.get(id=pk)
        if course:
            self.context = {
                'course': course
            }

        return render(request, self.template_name, context=self.context)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('id')
        course = Course.objects.get(id=pk)

        print(request.POST)
        print(request.POST.get("submit_button"))
        print(request.POST.get("delete_button"))

        if request.POST.get("submit_button") is None:
            course.delete()
            messages.success(request, course.title + " deleted successfully")
            return redirect('home')
        course.course_id = request.POST.get("course_code")
        course.title = request.POST.get("course_title")
        course.semester = request.POST.get("semester")
        course.deadline = request.POST.get("deadline")

        course.save()

        self.context = {
            'course': course
        }

        messages.success(request, course.title + " updated successfully")

        return render(request, self.template_name, context=self.context)


class ProposalSubmissionView(LoginRequiredMixin, View):
    template_name = 'project_management/proposal_submission.html'

    context = {
        ''
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        print(request.POST)

        return render(request, self.template_name, {})
