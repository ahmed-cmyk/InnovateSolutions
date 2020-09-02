from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail import send_mail
from DjangoUnlimited.settings import DEFAULT_FROM_EMAIL
from django.http import HttpResponseRedirect, JsonResponse

from Accounts.views import isValidated, get_user_type, number_symbol_exists
from .models import Student
from .forms import *
from Home.models import UserNotifications, send_html_mail
from re import search


def student_signup(request):
    if request.method == 'POST':
        user_form = InitialStudentForm(request.POST)
        if user_form.is_valid():
            if user_form.usernameExists():
                messages.warning(request, 'Username already taken. Try a different one.')  # checks if username exists
                # in db
                return redirect("student_registration")

            if user_form.emailExists():
                messages.warning(request, 'Email already taken. Try a different one.')  # checks if email exists in db
                return redirect("student_registration")

            if not user_form.same_passwords():
                messages.warning(request, 'Passwords not matching. Try again.')  # checks if password and confirm
                # password are matching
                return redirect("student_registration")

            if not user_form.email_domain_exists():
                messages.warning(request, 'Email domain does not exist. Try again.')  # checks if there is an existing
                # domain for given email
                return redirect("student_registration")

            else:
                if isValidated(user_form.cleaned_data.get('password1')):
                    student_form = StudentForm(request.POST, request.FILES)

                    if student_form.is_valid():
                        with transaction.atomic():
                            user = user_form.save()
                            student = student_form.save(commit=False)
                            student.user = user
                            email = str(student.user)
                            student.save()
                            student_form.save_m2m()

                            first_name = user_form.cleaned_data.get('first_name')
                            context = {'first_name': first_name}

                            subject = 'Your account creation request has been received'
                            htmlText = render_to_string('Accounts/account_creation_request.html', context)
                            send_html_mail(subject, htmlText, [email])

                            subject = 'New Student Account Created'
                            htmlText = f'A new student account for the user {email} has been created and is ' \
                                       f'currently pending approval.'
                            send_html_mail(subject, htmlText, [DEFAULT_FROM_EMAIL])

                        messages.success(request, 'A student account has been created')
                        return render(request, 'Accounts/pending_acc.html', get_user_type(request))
                    else:
                        messages.warning(request, student_form.errors.as_text)
                        return redirect('student_registration')

                else:
                    messages.warning(request, 'ERROR: Password must be 8 characters or more, and must have atleast 1 '
                                              'numeric character and 1 letter.')
                    return redirect("student_registration")
        else:
            messages.warning(request, user_form.errors.as_text)
            return redirect("student_registration")
    else:
        user_form = InitialStudentForm()
        student_form = StudentForm()
        user = get_user_type(request)
        args = {'student_form': student_form, 'user_form': user_form, 'user_type': user['user_type']}

        return render(request, 'Student/student_registration.html', args)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        student = Student.objects.get(user_id=request.user.id)
        user_form = EditStudentProfileInitialForm(request.POST, instance=request.user)
        student_form = EditStudentProfileForm(request.POST, request.FILES, instance=student)

        if user_form.is_valid() and student_form.is_valid():
            with transaction.atomic():
                user_form.save()
                student_form.save()
                return redirect('view_student_profile')
        else:
            messages.warning(request, student_form.errors.as_text)
            messages.warning(request, user_form.errors.as_text)
            return redirect('edit_student_profile')
    else:
        student = Student.objects.get(user_id=request.user.id)
        user_form = EditStudentProfileInitialForm(instance=request.user)
        student_form = EditStudentProfileForm(instance=student)
        args = {'student_form': student_form, 'user_form': user_form, 'user_type': "student", 'obj': student}
        return render(request, 'Student/edit_student_profile.html', args)


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
    return render(request, 'Student/view_student_profile.html', args)