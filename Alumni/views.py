from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from DjangoUnlimited.settings import DEFAULT_FROM_EMAIL
from django.urls import reverse

from Accounts.views import isValidated, get_user_type
from Home.models import send_html_mail
from .models import Alumni
from .forms import *


def signup(request):
    if request.method == 'POST':
        user_data = {'first_name': request.POST.get('first_name'),
                 'last_name': request.POST.get('last_name'),
                 'email': request.POST.get('email')}
        alumni_data = {'gender': request.POST.get('gender'),
                 'date_of_birth': request.POST.get('date_of_birth'),
                 'student_id': request.POST.get('student_id'),
                 'skills': request.POST.getlist('skills'),
                 'majors': request.POST.getlist('majors'),
                 'dp': request.FILES.get('dp'),
                 'cv': request.FILES.get('cv')}

        user_form = InitialAlumniForm(request.POST)

        if user_form.is_valid():
            if user_form.usernameExists():
                messages.warning(request, 'Username already taken. Try a different one.')  # checks if username exists in db
                user_form = InitialAlumniForm(user_data)
                alumni_form = AlumniForm(alumni_data)
                user = get_user_type(request)
                args = {'alumni_form': alumni_form, 'user_form': user_form, 'user_type': user['user_type']}
                return render(request, 'Alumni/alumni_registration.html', args)
                #return redirect("alumni_register")

            if user_form.emailExists():
                messages.warning(request, 'Email already taken. Try a different one.')  # checks if email exists in db
                user_form = InitialAlumniForm(user_data)
                alumni_form = AlumniForm(alumni_data)
                user = get_user_type(request)
                args = {'alumni_form': alumni_form, 'user_form': user_form, 'user_type': user['user_type']}
                return render(request, 'Alumni/alumni_registration.html', args)
                #return redirect("alumni_register")

            if not user_form.samePasswords():
                messages.warning(request, 'Passwords not matching. Try again.')  # checks if password and confirm
                # password are matching
                user_form = InitialAlumniForm(user_data)
                alumni_form = AlumniForm(alumni_data)
                user = get_user_type(request)
                args = {'alumni_form': alumni_form, 'user_form': user_form, 'user_type': user['user_type']}
                return render(request, 'Alumni/alumni_registration.html', args)
                #return redirect("alumni_register")

            if not user_form.emailDomainExists():
                messages.warning(request, 'Email domain does not exist. Try again.')  # checks if there is an exising
                # domain for given email
                user_form = InitialAlumniForm(user_data)
                alumni_form = AlumniForm(alumni_data)
                user = get_user_type(request)
                args = {'alumni_form': alumni_form, 'user_form': user_form, 'user_type': user['user_type']}
                return render(request, 'Alumni/alumni_registration.html', args)
                #return redirect("alumni_register")

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

                            first_name = user_form.cleaned_data.get('first_name')
                            context = {'first_name': first_name}
                            admin_context = {'first_name': first_name, 'protocol': 'http', 'domain': '127.0.0.1:8000'}

                            subject = 'Your account creation request has been received'
                            htmlText = render_to_string('Accounts/account_creation_request.html', context)
                            send_html_mail(subject, htmlText, [email])

                            subject = 'An account creation request has been received '
                            htmlText = render_to_string('Accounts/account_creation_request_admin.html', admin_context)
                            send_html_mail(subject, htmlText, [DEFAULT_FROM_EMAIL])

                        messages.success(request, 'Alumni account created')
                        return render(request, 'Accounts/pending_acc.html', get_user_type(request))

                    else:
                        messages.warning(request, alumni_form.errors.as_text)
                        user_form = InitialAlumniForm(user_data)
                        alumni_form = AlumniForm(alumni_data)
                        user = get_user_type(request)
                        args = {'alumni_form': alumni_form, 'user_form': user_form, 'user_type': user['user_type']}
                        return render(request, 'Alumni/alumni_registration.html', args)
                        #return redirect("alumni_register")

                else:
                    messages.warning(request,
                                     'ERROR: Password must be 8 characters or more, and must have atleast 1 numeric character and 1 letter.')
                    user_form = InitialAlumniForm(user_data)
                    alumni_form = AlumniForm(alumni_data)
                    user = get_user_type(request)
                    args = {'alumni_form': alumni_form, 'user_form': user_form, 'user_type': user['user_type']}
                    return render(request, 'Alumni/alumni_registration.html', args)
                    #return redirect("alumni_register")

        else:
            messages.warning(request, user_form.errors.as_text)
            user_form = InitialAlumniForm(user_data)
            alumni_form = AlumniForm(alumni_data)
            user = get_user_type(request)
            args = {'alumni_form': alumni_form, 'user_form': user_form, 'user_type': user['user_type']}
            return render(request, 'Alumni/alumni_registration.html', args)
            #return redirect("alumni_register")

    else:
        user_form = InitialAlumniForm()
        alumni_form = AlumniForm()
        user = get_user_type(request)
        args = {'alumni_form': alumni_form, 'user_form': user_form, 'user_type': user['user_type']}

        return render(request, 'Alumni/alumni_registration.html', args)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        alumni = Alumni.objects.get(user_id=request.user.id)
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
            return redirect('edit_alumni_profile')
    else:
        alumni = Alumni.objects.get(user_id=request.user.id)
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
