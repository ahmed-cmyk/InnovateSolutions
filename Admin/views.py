from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db import transaction
from django.contrib.admin.views.decorators import staff_member_required
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail import send_mail
from DjangoUnlimited.settings import SENDGRID_API_KEY
from django.utils import timezone
from datetime import timedelta, datetime, date
import csv
from django.http import HttpResponse

# Create your views here.

from Home.forms import CreateJobForm, EditJobForm
from Employer.forms import InitialEmployerForm, EmployerForm
from .forms import InitialAdminForm, AdminForm, AddIndustryForm, Statistics
from Accounts.views import isValidated, get_user_type, number_symbol_exists
from .models import Admin
from .forms import EditAdminProfileForm
from Student.forms import EditStudentProfileForm
from Student.models import Student, StudentJobApplication
from Home.models import Job
from Employer.models import Employer


# Create your views here.

@staff_member_required
def create_admin(request):
    if request.method == 'POST':
        user_form = InitialAdminForm(request.POST)

        if user_form.is_valid():
            if user_form.usernameExists():
                messages.info(request, 'Username already taken. Try a different one.') #checks if username exists in db
                return redirect("admin_register")

            elif user_form.emailExists():
                messages.info(request, 'Email already taken. Try a different one.') #checks if email exists in db
                return redirect("admin_register")

            elif number_symbol_exists(user_form.cleaned_data["first_name"]): #checks if number/symbol exists in string
                messages.info(request, 'Please enter a valid first name.')
                return redirect("admin_register")

            elif number_symbol_exists(user_form.cleaned_data["last_name"]): #checks if number/symbol exists in string
                messages.info(request, 'Please enter a valid last name.')
                return redirect("admin_register")

            elif not user_form.samePasswords():
                messages.info(request, 'Passwords not matching. Try again.') #checks if password and confirm password are matching
                return redirect("admin_register")

            elif not user_form.emailDomainExists(): #checks if there is an exising domain for given email
                messages.info(request, 'Email domain does not exist. Try again.')
                return redirect("admin_register")

            else:
                if isValidated(user_form.cleaned_data.get('password1')): #checks if password is valid
                    admin_form = AdminForm(request.POST, request.FILES)

                    if admin_form.is_valid():
                        with transaction.atomic():
                            user = user_form.save()
                            admin = admin_form.save(commit=False)
                            admin.user = user
                            admin.save()
                            next_page = request.POST.get('next', '/')
                            return redirect(next_page)
                    else:
                        messages.info(request, admin_form.errors)
                        return redirect("admin_register")
                else:
                    messages.info(request,
                                  'ERROR: Password must be 8 characters or more, and must have atleast 1 numeric character and 1 letter.')
                    return redirect("admin_register")
        else:
            messages.info(request, user_form.errors)
            return redirect("admin_register")
    else:
        user_form = InitialAdminForm()
        admin_form = AdminForm()
        args = {'admin_form': admin_form, 'user_form': user_form}
        return render(request, 'admin/admin_registration.html', args)


@staff_member_required
def view_profile(request):
    user = request.user
    hasAdminDetails = True
    try:
        admin = Admin.objects.get(user_id=user.id)
        args = {'admin': admin, 'user': user, 'hasAdminDetails': hasAdminDetails}
        return render(request, 'admin/view_admin_profile.html', args)
    except:
        if request.method == 'POST':
            admin_form = AdminForm(request.POST, request.FILES)

            if admin_form.is_valid():
                with transaction.atomic():
                    admin = admin_form.save(commit=False)
                    admin.user = user
                    admin.save()
                    return redirect(request.path_info)
            else:
                messages.info(request, admin_form.errors)
                return redirect(request.path_info)

        else:
            hasAdminDetails = False
            admin_form = AdminForm()
            args = {'admin_form': admin_form, 'hasAdminDetails': hasAdminDetails}
            return render(request, 'admin/view_admin_profile.html', args)


@staff_member_required
def edit_profile(request):
    admin = Admin.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        user_form = EditAdminProfileForm(request.POST, instance=request.user)
        admin_form = AdminForm(request.POST, request.FILES, instance=admin)

        if user_form.is_valid() and admin_form.is_valid():
            with transaction.atomic():
                user_form.save()
                admin_form.save()
                next_page = request.POST.get('next', '/')
                return redirect(next_page)
        else:
            messages.info(request, admin_form.errors)
            messages.info(request, user_form.errors)
            return redirect(request.path_info)
    else:
        user_form = EditAdminProfileForm(instance=request.user)
        admin_form = AdminForm(instance=admin)
        args = {'admin_form': admin_form, 'user_form': user_form}
        return render(request, 'admin/edit_admin_profile.html', args)


@staff_member_required
def create_job(request):
    admin = Admin.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        jobForm = CreateJobForm(request.POST, request.FILES)
        companyForm = EmployerForm(request.POST, request.FILES)

        if jobForm.is_valid() and companyForm.is_valid():
            with transaction.atomic():
                company = companyForm.save(commit=False)
                company.user_id = admin.user.id
                company.save()
                job = jobForm.save(commit=False)
                job.posted_by = request.user
                job.save()

                message = Mail(
                    from_email='info@murdochcareerportal.com',
                    to_emails=['sethshivangi1998@gmail.com'],
                    subject='New Job has been posted',
                    html_content="A new Job has been posted on the Murdoch Career Portal."
                )
                sg = SendGridAPIClient(SENDGRID_API_KEY)
                #   sg.send(message)

                for skill in request.POST.getlist('skills'):
                    job.skills.add(skill)

                next_page = request.POST.get('next', '/')
                return redirect(next_page)
        else:
            messages.info(request, jobForm.errors)
            return redirect(request.path_info)
    else:
        userForm = InitialEmployerForm()
        companyForm = EmployerForm()
        jobForm = CreateJobForm()

        args = {'companyForm': companyForm, 'jobForm': jobForm}
        return render(request, "admin/admin_create_job.html", args)


def export_stats_file(request, users, admins, students, current, alumni, employers, jobs_posted, apps, open_jobs, closed_jobs, deleted_jobs):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + date.today().strftime("%B %d %Y") + ".csv"
    writer = csv.writer(response)
    writer.writerow(['Type of Statistics', 'Count'])
    writer.writerow(['Total Users Signed Up', users])
    writer.writerow(['Administrators Signed Up', admins])
    writer.writerow(['Total Students Signed Up', students])
    writer.writerow(['Current Students Signed Up', current])
    writer.writerow(['Alumni Signed Up', alumni])
    writer.writerow(['Employers Signed Up', employers])
    writer.writerow(['Jobs Posted', jobs_posted])
    writer.writerow(['Student Applications', apps])
    writer.writerow(['Active Jobs', open_jobs])
    writer.writerow(['Jobs Closed and Filled by Murdoch Students', closed_jobs])
    writer.writerow(['Jobs Deleted', deleted_jobs])
    return response


@staff_member_required
def generate_statistics(request):
    user = get_user_type(request)
    if request.method == "POST":
        end_date = timezone.now()
        time = request.POST.get('period')
        if time == "Past 7 Days":
            start_date = end_date - timedelta(6)
        elif time == "Past 30 Days":
            start_date = end_date - timedelta(29)
        elif time == "Past Year":
            start_date = end_date - timedelta(364)

        users = User.objects.filter(date_joined__range=[start_date, end_date])
        admins = Admin.objects.filter(user_id__in=User.objects.filter(date_joined__range=[start_date, end_date]))
        admin_users = User.objects.filter(id__in=Admin.objects.all())
        students = Student.objects.filter(user_id__in=User.objects.filter(date_joined__range=[start_date, end_date]))
        current = Student.objects.filter(user_id__in=User.objects.filter(date_joined__range=[start_date, end_date]),
                                         alumni_status=False)
        alumni = Student.objects.filter(user_id__in=User.objects.filter(date_joined__range=[start_date, end_date]),
                                        alumni_status=True)
        employers = Employer.objects.filter(user_id__in=User.objects.filter(date_joined__range=[start_date, end_date])).exclude(user_id__in=admin_users)
        jobs_posted = Job.objects.filter(date_posted__range=[start_date, end_date])
        open_jobs = Job.objects.filter(date_posted__range=[start_date, end_date], status="Open")
        closed_jobs = Job.objects.filter(date_posted__range=[start_date, end_date], status="Closed")
        deleted_jobs = Job.objects.filter(date_posted__range=[start_date, end_date], status="Deleted")
        apps = StudentJobApplication.objects.filter(date_applied__range=[start_date, end_date])

        users = len(list(set(users)))
        admins = len(list(set(admins)))
        students = len(list(set(students)))
        current = len(list(set(current)))
        alumni = len(list(set(alumni)))
        employers = len(list(set(employers)))
        jobs_posted = len(list(set(jobs_posted)))
        open_jobs = len(list(set(open_jobs)))
        closed_jobs = len(list(set(closed_jobs)))
        deleted_jobs = len(list(set(deleted_jobs)))
        apps = len(list(set(apps)))

        args = {'users': users, 'admins': admins, 'students': students, 'current': current, 'alumni': alumni, 'employers': employers,
                'jobs_posted': jobs_posted, 'open_jobs': open_jobs, 'closed_jobs': closed_jobs,
                'deleted_jobs': deleted_jobs, 'apps': apps, 'user_type': user['user_type'], 'obj': user['obj']}

        return render(request, "admin/view_statistics.html", args)
    else:
        form = Statistics()
        args = {'form': form, 'user_type': user['user_type'], 'obj': user['obj']}
        return render(request, "admin/generate_statistics.html", args)