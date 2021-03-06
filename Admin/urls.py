from django.urls import path
from . import views

urlpatterns = [
    path('create_admin', views.create_admin, name='admin_register'),
    path('edit_admin_profile', views.edit_profile, name='edit_admin_profile'),
    path('view_admin_profile', views.view_profile, name='view_admin_profile'),
    path('view_pending_requests', views.view_pending, name='view_pending_requests'),
    path('view_pending_requests/<int:id>', views.view_pending, name='view_pending_requests'),
    path('view_account_details/<int:id>', views.view_pend_acc_profile, name='view_account_details'),
    path('change_status', views.change_accept_status, name='change_accept_status'),
    path('view_pending_jobs', views.view_pending_jobs, name='view_pending_jobs'),
    path('view_pending_jobs/<int:id>', views.view_pending_jobs, name='view_pending_jobs'),
    path('view_pending_job_details/<int:id>', views.view_pending_job_details, name='view_job_details'),
    path('change_job_status', views.change_job_status, name='change_job_status'),
    path('admin_create_job', views.create_job, name='admin_create_job'),
    path('statistics', views.generate_statistics, name='statistics'),
    path('job_statistics', views.generate_job_statistics, name='job_statistics'),
    path('student_statistics', views.generate_student_statistics, name='student_statistics'),
    path(
        'export_stats_file/<int:users>/<int:admins>/<int:students>/<int:current>/<int:alumni>/<int:employers>/<int:jobs_posted>/<int:apps>/<int:open_jobs>/<int:closed_jobs>/<int:deleted_jobs>/<int:total_users>/<int:pending_users>/<int:pending_jobs>/<int:alumni_apps>/<int:rejected_users>/<int:rejected_jobs>',
        views.export_stats_file, name='export_stats_file'),
    path('export_job_stats/<int:total_jobs>/<int:accepted_jobs>/<int:open_jobs>/<int:closed_jobs>/<int:deleted_jobs>/<int:pending_jobs>/<int:rejected_jobs>/<int:total_internships_posted>/<int:total_accepted_internships>/<int:open_internships>/<int:closed_internships>/<int:deleted_internships>/<int:pending_internships>/<int:rejected_internships>',
         views.export_job_stats, name='export_job_stats'),
    path('export_student_stats/<int:students>/<int:accepted_students>/<int:pending_students>/<int:rejected_students>/<int:alumni>/<int:accepted_alumni>/<int:pending_alumni>/<int:rejected_alumni>',
         views.export_student_stats, name='export_student_stats'),
    path('view_employer_profile/<int:id>', views.view_employer_profile, name='admin_view_employer_profile'),
    path('edit_employer_profile/<int:id>', views.edit_employer_profile, name='admin_edit_employer_profile'),
    path('edit_student_profile/<int:id>', views.edit_student_profile, name='admin_edit_student_profile'),
    path('view_student_profile/<int:id>', views.view_student_profile, name='admin_view_student_profile'),
    path('edit_alumni_profile/<int:id>', views.edit_alumni_profile, name='admin_edit_alumni_profile'),
    path('view_alumni_profile/<int:id>', views.view_alumni_profile, name='admin_view_alumni_profile'),
    path('', views.backup_database, name="backup_database"),
    path('download-source-code', views.download_source_code, name="download-source-code")
]
