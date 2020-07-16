from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db import transaction
from django.contrib.auth.decorators import login_required
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail import send_mail
from DjangoUnlimited.settings import DEFAULT_FROM_EMAIL
from django.http import HttpResponseRedirect, JsonResponse

from Accounts.views import isValidated, get_user_type, number_symbol_exists
from .models import Student
from .forms import *
from Home.models import UserNotifications
from re import search


def student_signup(request):
    if request.method == 'POST':
        user_form = InitialStudentForm(request.POST)
        if user_form.is_valid():
            student_form = StudentForm(request.POST, request.FILES)
            
            if student_form.is_valid():
                with transaction.atomic():
                    user = user_form.save()
                    student = student_form.save(commit=False)
                    student.user = user
                    email = str(student.user)
                    student.save()
                    student_form.save_m2m()

                    send_mail('New Job has been posted',
                              "A new student account with username '{{ user.get_username }}' has been posted on the "
                              "Murdoch Career Portal.",
                              DEFAULT_FROM_EMAIL, [email],
                              fail_silently=False)

                messages.success(request, 'A student account has been created')
                return redirect('log_in')
            else:
                return redirect('student_registration')
        else:
            messages.error(request, user_form.errors)
            return redirect("student_registration")
    else:
        user_form = InitialStudentForm()
        student_form = StudentForm()
        user = get_user_type(request)
        args = {'student_form': student_form, 'user_form': user_form, 'user_type': user['user_type']}

        return render(request, 'Student/student_registration.html', args)


@login_required
def edit_profile(request):
    student = Student.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        user_form = EditStudentProfileInitialForm(request.POST, instance=request.user)
        student_form = EditStudentProfileForm(request.POST, request.FILES, instance=student)

        if user_form.is_valid() and student_form.is_valid():
            with transaction.atomic():
                user_form.save()
                student_form.save()
                return redirect('view_student_profile')
        else:
            messages.error(request, student_form.errors)
            messages.error(request, user_form.errors)
            return redirect("edit_student_profile")
    else:
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