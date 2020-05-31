from django.urls import path
from . import views

urlpatterns = [
    path('student_registration', views.student_signup, name='student_registration'),
    path('edit_student_profile', views.edit_profile, name='edit_student_profile'),
    path('view_student_profile', views.view_profile, name='view_student_profile'),
]