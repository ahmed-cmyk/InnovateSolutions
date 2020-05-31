from django.urls import path

from .views import HelpDeskFormView, HelpDeskRequests, MyHelpDeskRequests

urlpatterns = [
    path('', HelpDeskFormView.as_view(), name='HelpDesk'),
    path('<int:pk>', HelpDeskFormView.as_view(), name='HelpDesk'),
    path('requests', HelpDeskRequests.as_view(), name='HelpDeskRequests'),
    path('myrequests', MyHelpDeskRequests.as_view(), name='MyHelpDeskRequests'),

]
