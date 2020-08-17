from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_job', views.create_job, name='create_job'),
    path('view_jobs', views.view_jobs, name='view_jobs'),
    path('my_applications', views.my_applications, name='my_applications'),
    path('job_details/<int:id>', views.job_details, name='job_details'),
    path('edit_job/<int:id>', views.edit_job, name='edit_job'),
    path('delete_job/<int:id>', views.delete_job, name='delete_job'),
    path('close_job/<int:id>', views.close_job, name='close_job'),
    path('reopen_job/<int:id>', views.reopen_job, name='reopen_job'),
    path('view_students', views.view_students, name='view_students'),
    path('view_alumni', views.view_alumni, name='view_alumni'),
    path('student_details/<int:id>', views.student_details, name='student_details'),
    path('alumni_details/<int:id>', views.alumni_details, name='alumni_details'),
    path('job_to_student_skills/<int:id>', views.job_to_student_skills, name='job_to_student_skills'),
    path('job_to_alumni_skills/<int:id>', views.job_to_alumni_skills, name='job_to_alumni_skills'),
    path('get_student_cv_file/<int:id>', views.get_student_cv_file, name='get_student_cv_file'),
    path('get_alumni_cv_file/<int:id>', views.get_alumni_cv_file, name='get_alumni_cv_file'),
    path('terms', views.terms, name='terms'),
    path('faq', views.faq, name='faq'),
    path('anti_scam', views.anti_scam, name='anti_scam'),
    path('privacy', views.privacy, name='privacy'),
    path('sitemap', views.sitemap, name='sitemap'),
]
