from django.urls import path
from . import views
from Employer.views import get_employer_trade_license

urlpatterns = [
    path('alumni_registration', views.signup, name='alumni_register'),
    path('edit_alumni_profile', views.edit_profile, name='edit_alumni_profile'),
    path('view_alumni_profile', views.view_profile, name='view_alumni_profile'),
    path('validate_username', views.check_username, name="check_alumni_username"),
    path('get_employer_trade_license/<int:id>', get_employer_trade_license, name='get_employer_trade_license'),
]
