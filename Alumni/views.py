from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db import transaction
from django.contrib.auth.decorators import login_required
from DjangoUnlimited.settings import DEFAULT_FROM_EMAIL

from Accounts.views import isValidated, get_user_type
from Home.models import send_html_mail
from .models import Alumni
from .forms import *


def signup(request):
    if request.method == 'POST':
        user_form = InitialAlumniForm(request.POST)

        if user_form.is_valid():
            if user_form.usernameExists():
                messages.warning(request, 'Username already taken. Try a different one.')  # checks if username exists
                # in db
                return redirect("alumni_register")

            if user_form.emailExists():
                messages.warning(request, 'Email already taken. Try a different one.')  # checks if email exists in db
                return redirect("alumni_register")

            if not user_form.samePasswords():
                messages.warning(request, 'Passwords not matching. Try again.') # checks if password and confirm
                # password are matching
                return redirect("alumni_register")

            if not user_form.emailDomainExists():
                messages.warning(request, 'Email domain does not exist. Try again.')  # checks if there is an exising
                # domain for given email
                return redirect("alumni_register")

            else:
                if isValidated(user_form.cleaned_data.get('password1')):  # checks if password is valid
                    alumni_form = AlumniForm(request.POST, request.FILES)

                    if alumni_form.is_valid():
                        with transaction.atomic():
                            user = user_form.save()
                            alumni = alumni_form.save(commit=False)
                            alumni.user = user
                            email = str(alumni.user)
                            alumni.save()
                            alumni_form.save_m2m()

                            subject = 'Account Created'
                            htmlText = 'Your account has been created and is currently pending approval'
                            send_html_mail(subject, htmlText, [email])

                            subject = 'New Alumni Account Created'
                            htmlText = f'A new alumni account for the user {email} has been created and is ' \
                                       f'currently pending approval.'
                            send_html_mail(subject, htmlText, [DEFAULT_FROM_EMAIL])

                        messages.success(request, 'Alumni account created')
                        return render(request, 'Accounts/pending_acc.html', get_user_type(request))

                    else:
                        messages.warning(request, alumni_form.errors.as_text)
                        return redirect("alumni_register")

                else:
                    messages.warning(request,
                                  'ERROR: Password must be 8 characters or more, and must have atleast 1 numeric character and 1 letter.')
                    return redirect("alumni_register")

        else:
            messages.warning(request, user_form.errors.as_text)
            return redirect("alumni_register")

    else:
        user_form = InitialAlumniForm()
        alumni_form = AlumniForm()
        user = get_user_type(request)
        args = {'alumni_form': alumni_form, 'user_form': user_form, 'user_type': user['user_type']}

        return render(request, 'Alumni/alumni_registration.html', args)


@login_required
def edit_profile(request):
    alumni = Alumni.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        user_form = EditAlumniProfileInitialForm(request.POST, instance=request.user)
        alumni_form = EditAlumniProfileForm(request.POST, request.FILES, instance=alumni)

        if user_form.is_valid() and alumni_form.is_valid():
            with transaction.atomic():
                user_form.save()
                alumni_form.save()

                messages.success(request, 'Profile edit was successful')
                return redirect('view_alumni_profile')
        else:
            messages.warning(request, alumni_form.errors.as_text)
            messages.warning(request, user_form.errors.as_text)
            return redirect("edit_alumni_profile")
    else:
        user_form = EditAlumniProfileInitialForm(instance=request.user)
        alumni_form = EditAlumniProfileForm(instance=alumni)
        args = {'alumni_form': alumni_form, 'user_form': user_form, 'user_type': "alumni", 'obj': alumni}
        return render(request, 'Alumni/edit_alumni_profile.html', args)


def check_username(request):
    if request.is_ajax and request.method == 'GET':
        email = request.GET.get("username", None)
        if User.objects.filter(username=email).exists():
            return JsonResponse({"valid": False}, status=200)
        else:
            return JsonResponse({"valid": True}, status=200)

    return JsonResponse({}, status=400)


@login_required
def view_profile(request):
    user = request.user
    u = get_user_type(request)
    args = {'user': user, 'user_type': u['user_type'], 'obj': u['obj']}
    return render(request, 'Alumni/view_alumni_profile.html', args)
