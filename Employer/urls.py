from django.urls import path
from . import views

urlpatterns = [
    path('employer_registration', views.signup, name='employer_register'),
    path('edit_employer_profile', views.edit_profile, name='edit_employer_profile'),
    path('view_employer_profile', views.view_profile, name='view_employer_profile'),
    path('validate_username', views.check_username, name="check_employer_username"),
    path('activate', views.activate, name='activate'),
    path('get_employer_trade_license/<int:id>', views.get_employer_trade_license, name='get_employer_trade_license'),
]
