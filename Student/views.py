from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db import transaction
from django.contrib.auth.decorators import login_required
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail import send_mail
from DjangoUnlimited.settings import SENDGRID_API_KEY, DEFAULT_FROM_EMAIL 

# Create your views here.

from Accounts.views import isValidated, get_user_type, number_symbol_exists
from .models import Student
from .forms import *
from Home.models import UserNotifications
from re import search


def student_signup(request):
    if request.method == 'POST':
        user_form = InitialStudentForm(request.POST)
        if user_form.is_valid():
            if user_form.usernameExists(): #checks if username exists in db
                messages.info(request, 'Username already taken. Try a different one.')
                return redirect("student_registration")

            elif user_form.emailExists(): #checks if email exists in db
                messages.info(request, 'Email already taken. Try a different one.')
                return redirect("student_registration")

            elif number_symbol_exists(user_form.cleaned_data["first_name"]): #checks if number/symbol exists in string
                messages.info(request, 'Please enter a valid first name.')
                return redirect("student_registration")

            elif number_symbol_exists(user_form.cleaned_data["last_name"]): #checks if number/symbol exists in string
                messages.info(request, 'Please enter a valid last name.')
                return redirect("student_registration")

            elif not user_form.samePasswords(): #checks if password and confirm password are matching
                messages.info(request, 'Passwords not matching. Try again.')
                return redirect("student_registration")

            elif not user_form.emailDomainExists(): #checks if there is an exising domain for given email
                messages.info(request, 'Email domain does not exist. Try again.')
                return redirect("student_registration")
            else:
                if isValidated(user_form.cleaned_data.get('password1')): #checks if password is valid
                    student_form = StudentForm(request.POST, request.FILES)
                    if student_form.is_valid():
                        email = user_form.cleaned_data["email"]

                        if not search("@student.murdoch.edu.au", email):
                            if not student_form.cleaned_data["alumni_status"]:
                                messages.info(request, 'Please enter an existing murdoch student email.')
                                return redirect("student_registration")
                            else:
                                pass

                        with transaction.atomic():
                            user = user_form.save()
                            student = student_form.save(commit=False)
                            student.user = user
                            student.save()
                            student_form.save_m2m()

                            message = Mail(
                                from_email=DEFAULT_FROM_EMAIL,
                                to_emails=['ict302jan2020@gmail.com'],
                                subject='New User has signed up',
                                html_content="A new Student has registered to use the Murdoch Career Portal."
                            )
                            sg = SendGridAPIClient(SENDGRID_API_KEY)
                            # sg.send(message)

                          #  notification = "A new Student has registered to use the Murdoch Career Portal."
                           # add_notif = UserNotifications(to_user_id=1, from_user_id=request.user.id,
                                                     #     notification=notification,
                                                      #    type='Sign Up',
                                                      #    to_show=True)
                           # add_notif.save()
                            messages.success(request, "Student Account Successfully Created !", extra_tags="student_account_activated")
                            return redirect("log_in")
                    else:
                        messages.info(request, student_form.errors)
                        return redirect("student_registration")
                else:
                    messages.info(request, 
                                    'ERROR: Password must be 8 characters or more, and must have atleast 1 numeric character and 1 letter.')
                    return redirect("student_registration")
        else:
            messages.info(request, user_form.errors)
            return redirect("student_registration")
    else:
        user_form = InitialStudentForm()
        student_form = StudentForm()
        user = get_user_type(request)
        args = {'student_form': student_form, 'user_form': user_form, 'user_type': user['user_type']}

        return render(request, 'student_registration.html', args)

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
            print(student_form)
            messages.info(request, student_form.errors)
            messages.info(request, user_form.errors)
            return redirect("edit_student_profile")
    else:
        user_form = EditStudentProfileInitialForm(instance=request.user)
        student_form = EditStudentProfileForm(instance=student)
        args = {'student_form': student_form, 'user_form': user_form, 'user_type': "student", 'obj': student}
        return render(request, 'edit_student_profile.html', args)

@login_required
def view_profile(request):
    user = request.user
    u = get_user_type(request)
    args = {'user': user, 'user_type': u['user_type'], 'obj': u['obj']}
    return render(request, 'view_student_profile.html', args)