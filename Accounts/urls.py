from django.urls import path, include, re_path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup', views.signup, name='sign_up'),
    path('login', views.login, name='log_in'),
    path('ForgotPassword', views.forgot_password, name='forgot_password'),
    path('logout', views.logout, name='logout'),

    re_path(
        r'^password_reset/$',
        auth_views.PasswordResetView.as_view(template_name='Accounts/password_reset_form.html',
                                             subject_template_name='registration/password_reset_subject.txt'),
        name='password_reset'
    ),
    re_path(
        r'^password_reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='Accounts/password_link_sent.html', ),
        name='password_reset_done'
    ),
    re_path(
        r'^password_reset/confirm/(?P<uidb64>[\w-]+)/(?P<token>[\w-]+)/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='Accounts/password_reset_confirm.html'),
        name='password_reset_confirm',
    ),
    re_path(
        r'^password_reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='Accounts/password_reset_complete.html'),
        name='password_reset_complete',
    )

]
