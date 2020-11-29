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
        user_data = {'first_name': request.POST.get('first_name'),
                 'last_name': request.POST.get('last_name'),
                 'email': request.POST.get('email')}
        student_data = {'gender': request.POST.get('gender'),
                 'date_of_birth': request.POST.get('date_of_birth'),
                 'student_id': request.POST.get('student_id'),
                 'expected_graduation_date': request.POST.get('expected_graduation_date'),
                 'personal_email': request.POST.get('personal_email'),
                 'skills': request.POST.getlist('skills'),
                 'majors': request.POST.getlist('majors'),
                 'dp': request.FILES.get('dp'),
                 'cv': request.FILES.get('cv')}

        user_form = InitialStudentForm(request.POST)
        if user_form.is_valid():
            if user_form.usernameExists():
                messages.error(request, 'Username already taken. Try a different one.', extra_tags='danger')  # checks if username exists in db

            elif user_form.emailExists():
                messages.error(request, 'Email already taken. Try a different one.', extra_tags='danger')  # checks if email exists in db

            elif not user_form.same_passwords():
                messages.error(request, 'Passwords not matching. Try again.', extra_tags='danger')  # checks if password and confirm password are matching

            elif not user_form.email_domain_exists():
                messages.error(request, 'Email domain does not exist. Try again.', extra_tags='danger')  # checks if there is an existing domain for given email
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
                            admin_context = {'first_name': first_name, 'protocol': 'https', 'domain': 'murdochdubaicareerportal.com'}

                            subject = 'Your account creation request has been received'
                            htmlText = render_to_string('Accounts/account_creation_request.html', context)
                            send_html_mail(subject, htmlText, [email])

                            subject = 'An account creation request has been received '
                            htmlText = render_to_string('Accounts/account_creation_request_admin.html', admin_context)
                            send_html_mail(subject, htmlText, [DEFAULT_FROM_EMAIL])

                        messages.success(request, 'A student account has been created')
                        return render(request, 'Accounts/pending_acc.html', get_user_type(request))
                    else:
                        messages.error(request, student_form.errors, extra_tags='danger')
                else:
                    messages.error(request, 'Password must be 8 characters or more, and must have at least 1 numeric character '
                                            'and 1 letter.', extra_tags='danger')
        else:
            messages.error(request, user_form.errors, extra_tags='danger')

        user_form = InitialStudentForm(user_data)
        student_form = StudentForm(student_data)
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
            messages.error(request, student_form.errors, extra_tags='danger')
            messages.error(request, user_form.errors, extra_tags='danger')
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