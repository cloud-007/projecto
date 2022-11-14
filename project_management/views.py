from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from accounts.models import Teacher
from project_management.models import Course


class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()
        return render(request, self.template_name, {'courses': courses})

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class ProjectDetailsView(LoginRequiredMixin, View):
    template_name = 'project_management/project_details.html'

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
        context = {
            'course': course,
            'proposals': proposals,
            'filter_by': filter_by,
            'teachers': Teacher.objects.all()
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class CreateNewCourse(LoginRequiredMixin, View):
    template_name = 'project_management/create_new_course.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        course = Course()
        print(request)
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

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('id')
        semester = kwargs.get('semester')
        print(kwargs)
        print(id)
        print(semester)
        course = Course.objects.get(id=pk)
        if course:
            print(course)
            context = {
                'course': course
            }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        course_id = request.POST.get("course_code")
        title = request.POST.get("course_title")
        semester = request.POST.get("semester")
        deadline = request.POST.get("deadline")

        course = Course.objects.filter(course_id=course_id, semester=semester).first()

        context = {
            'course': course
        }

        course.course_id = course_id
        course.title = title
        course.semester = semester
        course.deadline = deadline

        course.save()
        messages.success(request, course.title + " updated successfully")
        return redirect('home')
