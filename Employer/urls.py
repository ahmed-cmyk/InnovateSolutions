from django.urls import path
from . import views

urlpatterns = [
    path('employer_registration', views.signup, name='employer_register'),
    path('edit_employer_profile', views.edit_profile, name='edit_employer_profile'),
    path('view_employer_profile', views.view_profile, name='view_employer_profile'),
    path('validate_username', views.check_username, name="check_employer_username"),
]
