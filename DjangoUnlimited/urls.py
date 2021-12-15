from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers

from Admin.views import download_file

router = routers.SimpleRouter()

urlpatterns = [
    path('', include('Home.urls')),
    path('admin/backups/', include('dbbackup_ui.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('Accounts.urls')),
    path('alumni/', include('Alumni.urls')),
    path('my_admin/', include('Admin.urls')),
    path('student/', include('Student.urls')),
    path('employer/', include('Employer.urls')),
    path('HelpDesk/', include('HelpDesk.urls')),
    path('bulletin/', include('Bulletin.urls')),  # Using URLS from the Bulletin app
    path('backup/<str:filename>', download_file, name="backup_download"),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
                            static(settings.BACKUP_URL, document_root=settings.BACKUP_ROOT)
