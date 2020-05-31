from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('create_admin', views.create_admin, name='admin_register'),
    path('edit_admin_profile', views.edit_profile, name='edit_admin_profile'),
    path('view_admin_profile', views.view_profile, name='view_admin_profile'),
    path('admin_create_job', views.create_job, name='admin_create_job'),
    path('statistics', views.generate_statistics, name='statistics'),
    path('export_stats_file/<int:users>/<int:admins>/<int:students>/<int:current>/<int:alumni>/<int:employers>/<int:jobs_posted>/<int:apps>/<int:open_jobs>/<int:closed_jobs>/<int:deleted_jobs>', views.export_stats_file, name='export_stats_file')
]
