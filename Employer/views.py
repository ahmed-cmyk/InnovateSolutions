from django.http import HttpResponse, JsonResponse
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
from Home.models import UserNotifications, send_html_mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail import send_mail
from DjangoUnlimited.settings import DEFAULT_FROM_EMAIL

import os
import csv


def signup(request):
    if request.method == 'POST':
        user_form = InitialEmployerForm(request.POST)

        if user_form.is_valid():
            if user_form.usernameExists():
                messages.info(request,
                              'Username already taken. Try a different one.')  # checks if username exists in db
                return redirect("employer_register")

            elif user_form.emailExists():
                messages.info(request, 'Email already taken. Try a different one.')  # checks if email exists in db
                return redirect("employer_register")

            elif not user_form.samePasswords():
                messages.info(request,
                              'Passwords not matching. Try again.')  # checks if password and confirm password are matching
                return redirect("employer_register")

            elif not user_form.emailDomainExists():
                messages.info(request,
                              'Email domain does not exist. Try again.')  # checks if there is an exising domain for given email
                return redirect("employer_register")

            else:
                if isValidated(user_form.cleaned_data.get('password1')):  # checks if password is valid
                    employer_form = EmployerForm(request.POST, request.FILES)

                    if employer_form.is_valid():
                        with transaction.atomic():
                            user = user_form.save()
                            employer = employer_form.save(commit=False)
                            employer.user = user
                            email = str(request.user)
                            employer.save()

                            # send_mail(
                            #     'New User has signed up',
                            #     "A new Employer has registered to use the Murdoch Career Portal.",
                            #     DEFAULT_FROM_EMAIL, [email],
                            #     fail_silently=True
                            # )
                            subject = 'New User has signed up'
                            htmlText = "A new Employer has registered to use the Murdoch Career Portal."
                            send_html_mail(subject, htmlText, [email])

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


def check_username(request):
    if request.is_ajax and request.method == 'GET':
        email = request.GET.get("username", None)
        if User.objects.filter(username=email).exists():
            return JsonResponse({"valid": False}, status=200)
        else:
            return JsonResponse({"valid": True}, status=200)

    return JsonResponse({}, status=400)


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
