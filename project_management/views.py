from django.shortcuts import render
from django.views import View

from project_management.models import Course


class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        objects = Course.objects.all()
        return render(request, self.template_name, {'objects': objects})

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class ProjectDetailsView(View):
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
            'proposals': proposals
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
