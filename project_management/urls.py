from django.urls import path

from .views import ProjectDetailsView, CreateNewCourse, UpdateCourseView, ProposalSubmissionView, ProposalUpdateView

urlpatterns = [
    path('project/create_new', CreateNewCourse.as_view(), name='create-new-course'),
    path('project/<int:id>/<str:filter_by>', ProjectDetailsView.as_view(), name='course-details'),
    path('project/<int:id>/<str:semester>/update', UpdateCourseView.as_view(), name='course-update'),
    path('project/<int:id>/<str:semester>/<int:proposal_id>/update', ProposalUpdateView.as_view(),
         name='proposal-update'),
    path('project/<int:id>/<str:semester>/proposal-submission', ProposalSubmissionView.as_view(),
         name='proposal-submission'),
]
