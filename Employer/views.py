from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db import transaction
from django.contrib.auth.decorators import login_required

# Create your views here.

from Accounts.views import isValidated, get_user_type
from .models import Employer
from .forms import InitialEmployerForm, EmployerForm
from Student.models import Student
from Admin.models import Admin
from Home.models import UserNotifications
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail import send_mail
from DjangoUnlimited.settings import SENDGRID_API_KEY, DEFAULT_FROM_EMAIL

import os
import csv


def signup(request):
    if request.method == 'POST':
        user_form = InitialEmployerForm(request.POST)

        if user_form.is_valid():
            if user_form.usernameExists():
                messages.info(request, 'Username already taken. Try a different one.') #checks if username exists in db
                return redirect("employer_register")

            elif user_form.emailExists():
                messages.info(request, 'Email already taken. Try a different one.') #checks if email exists in db
                return redirect("employer_register")

            elif not user_form.samePasswords():
                messages.info(request, 'Passwords not matching. Try again.') #checks if password and confirm password are matching
                return redirect("employer_register")

            elif not user_form.emailDomainExists():
                messages.info(request, 'Email domain does not exist. Try again.') #checks if there is an exising domain for given email
                return redirect("employer_register")

            else:
                if isValidated(user_form.cleaned_data.get('password1')): #checks if password is valid
                    employer_form = EmployerForm(request.POST, request.FILES)

                    if employer_form.is_valid():
                        with transaction.atomic():
                            user = user_form.save()
                            employer = employer_form.save(commit=False)
                            employer.user = user
                            employer.save()

                            message = Mail(
                                from_email=DEFAULT_FROM_EMAIL,
                                to_emails=['ict302jan2020@gmail.com'],
                                subject='New User has signed up',
                                html_content="A new Employer has registered to use the Murdoch Career Portal."
                            )
                            sg = SendGridAPIClient(SENDGRID_API_KEY)
                           # sg.send(message)

                        #  notification = "A new Employer has registered to use the Murdoch Career Portal."
                        # add_notif = UserNotifications(to_user_id=1, from_user_id=request.user.id,
                        #       notification=notification,
                        #     type='Sign Up',
                        #     to_show=True)
                        #  add_notif.save()

                        return redirect("log_in")
                    else:
                        messages.info(request, employer_form.errors)
                        return redirect("employer_register")
                else:
                    messages.info(request,
                                  'ERROR: Password must be 8 characters or more, and must have atleast 1 numeric character and 1 letter.')
                    return redirect("employer_register")
        else:
            messages.info(request, user_form.errors)
            return redirect("employer_register")
    else:
        user_form = InitialEmployerForm()
        employer_form = EmployerForm()
        user = get_user_type(request)
        args = {'employer_form': employer_form, 'user_form': user_form, 'user_type': user['user_type']}
        return render(request, 'Employer/employer_registration.html', args)


@login_required
def edit_profile(request):
    args = get_user_type(request)
    if args['obj'] is not None:
        if request.method == 'POST':
            form = EmployerForm(request.POST, request.FILES, instance=args['obj'])

            if form.is_valid():
                form.save()
                return redirect('view_employer_profile')
            else:
                messages.info(request, form.errors)
                return redirect("edit_employer_profile")
        else:
            form = EmployerForm(instance=args['obj'])
            args = {'employer_form': form, 'obj': args['obj'], 'user_type': args['user_type']}
            return render(request, 'Employer/edit_employer_profile.html', args)
    else:
        messages.info(request, 'This employer user does not exist')


@login_required
def view_profile(request):
    return render(request, 'Employer/view_employer_profile.html', get_user_type(request))
