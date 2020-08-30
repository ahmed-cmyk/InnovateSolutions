"""DjangoUnlimited URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from Admin.views import download_file

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

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.BACKUP_URL,
                                                                                                   document_root=settings.BACKUP_ROOT)
