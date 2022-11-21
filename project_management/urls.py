from django.urls import path

from .views import ProjectDetailsView, CreateNewCourse, UpdateCourseView, ProposalSubmissionView, ProposalUpdateView, \
    MarkingStudentView

urlpatterns = [
    path('create_new', CreateNewCourse.as_view(), name='create-new-course'),
    path('<int:id>/<str:filter_by>', ProjectDetailsView.as_view(), name='course-details'),
    path('<int:id>/<str:semester>/update', UpdateCourseView.as_view(), name='course-update'),
    path('<int:id>/<str:semester>/<int:proposal_id>/update', ProposalUpdateView.as_view(),
         name='proposal-update'),
    path('<int:id>/<str:semester>/proposal-submission', ProposalSubmissionView.as_view(),
         name='proposal-submission'),
    path('<int:id>/<int:proposal_id>/mark/', MarkingStudentView.as_view(),
         name='marking-student'),

]
