from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from project_management.views import HomeView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', HomeView.as_view(), name='home'),
                  path('', include('accounts.urls'), name='accounts'),
                  path('', include('project_management.urls'), name='home')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
