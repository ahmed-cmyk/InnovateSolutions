from django.urls import path
from . import views

urlpatterns = [
	path('alumni_registration', views.signup, name='alumni_register'),
	path('edit_alumni_profile', views.edit_profile, name='edit_alumni_profile'),
    path('view_alumni_profile', views.view_profile, name='view_alumni_profile')
]