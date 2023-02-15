from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from project_management.views import HomeView, NoticeBoardView, NoticeDetailView, NoticeCreateView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', HomeView.as_view(), name='home'),
                  path('accounts/', include('accounts.urls'), name='accounts'),
                  path('project/', include('project_management.urls')),
                  path('notices/', NoticeBoardView.as_view(), name='notice-list'),
                  path('notice/<int:pk>/', NoticeDetailView.as_view(), name='notice-detail'),
                  path('notice/create/', NoticeCreateView.as_view(), name='notice-create'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
